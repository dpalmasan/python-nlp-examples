from collections import defaultdict
import random
from typing import Dict, List, Union


class HMMGenerator:
    START_SYMBOL = "<S>"
    END_SYMBOL = "</S>"

    def __init__(self, ngram_length=2):
        self._trained = False
        self._ngram_length = ngram_length
        self._probs: Dict[str, float] = defaultdict(float)
        self._context: Dict[str, List[str]] = defaultdict(list)

    @property
    def probs(self) -> Dict[str, int]:
        return dict(self._probs)

    @property
    def ngram_length(self) -> int:
        return self._ngram_length

    def _train_validation(self):
        if not self._trained:
            raise Exception("Needs to be trained!")

    def train(self, sents):
        for sent in filter(lambda x: len(x) > 0, sents):
            new_sent = (
                [HMMGenerator.START_SYMBOL] * (self.ngram_length - 1)
                + sent
                + [HMMGenerator.END_SYMBOL]
            )
            for i in range(len(new_sent)):
                if i + self.ngram_length > len(new_sent):
                    break
                ngram = tuple(word for word in new_sent[i:i + self.ngram_length])
                word = ngram[-1]
                self._probs[ngram] += 1
                context = ngram[:-1]
                self._context[context].append(word)
        for ngram, count in self._probs.items():
            self._probs[ngram] = count / len(self._context[ngram[:-1]])

        self._trained = True

    def generate_random_sentence(self) -> str:
        tokens = []
        current_token = HMMGenerator.START_SYMBOL
        ngram_prev = (HMMGenerator.START_SYMBOL,) *(self.ngram_length - 1)
        while True:
            candidate_tokens = []
            for candidate in self._context[ngram_prev]:
                candidate_tokens.append((candidate, self._probs[(*ngram_prev, candidate)]))

            prob = random.random()
            cum_prob = 0
            for candidate in candidate_tokens:
                cum_prob += candidate[1]
                if cum_prob >= prob:
                    current_token = candidate[0]
                    break

            if current_token == HMMGenerator.END_SYMBOL:
                break
            tokens.append(current_token)
            ngram_prev = (*ngram_prev[1:], current_token)
        return " ".join(tokens)
        


