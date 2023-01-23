from abc import abstractmethod
from pathlib import Path
from typing import Dict
from collections import defaultdict
from typing import Iterable
import re


class Tokenizer:
    @abstractmethod
    def tokenize(self, text: str) -> Iterable[str]:
        pass


class LemmaTokenizer(Tokenizer):
    def __init__(self, lemmas: Dict[str, str], threshold: int = 3):
        self._lemmas = lemmas
        self._re = re.compile("[^0-9a-zA-Z]+")
        self._threshold = threshold

    def tokenize(self, text: str) -> Iterable[str]:
        return [
            self._lemmas.get(word.lower(), word.lower())
            for word in self._re.sub(" ", text).split()
            if len(word) >= self._threshold
        ]

    @classmethod
    def load_from_file(cls, filepath: Path):
        lexicon = {}
        with open(filepath, "r") as fp:
            for line in fp:
                lemma, word = line.split()
                lexicon[word.strip()] = lemma.strip()

        return cls(lexicon)


class InMemoryInvertedIndex:
    def __init__(self, docs: Iterable[str], tokenizer: Tokenizer):
        self._terms = defaultdict(list)
        self._build_terms(docs, tokenizer)
        self._tokenizer = tokenizer

    def _build_terms(self, docs, tokenizer) -> None:
        for i, doc in enumerate(docs):
            curr_term = None
            for term in sorted(tokenizer.tokenize(doc)):
                if term != curr_term:
                    self._terms[term].append(i)
                    curr_term = term

    def search(self, query: str) -> Iterable[int]:
        terms = self._tokenizer.tokenize(query)
        return self._intersect(terms)

    def _intersect(self, terms) -> Iterable[int]:
        # Sort by frequency
        terms = sorted(terms, key=lambda x: len(self._terms[x]))
        curr_term = 0
        result = self._terms[terms[curr_term]]
        curr_term += 1
        while curr_term < len(terms) and result:
            result = self._intersect_two(result, self._terms[terms[curr_term]])
            curr_term += 1

        return result

    def _intersect_two(self, p1, p2):
        i1 = 0
        i2 = 0
        answer = []
        while i1 < len(p1) and i2 < len(p2):
            if p1[i1] == p2[i2]:
                answer.append(p1[i1])
                i1 += 1
                i2 += 2
            else:
                if p1[i1] < p2[i2]:
                    i1 += 1
                else:
                    i2 += 1
        return answer
