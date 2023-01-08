import re
from data import stopwords

from collections import defaultdict
import re


def clean_text(text):
    new_text = re.sub(r"[^a-zA-Záéíóú ]", "", text)
    return new_text.replace("Web", "")


def get_ngrams(text, n: int = 1):
    tokens = text.split(" ")
    return [tuple(tokens[j : j + n]) for j in range(len(tokens) - n + 1)]


def candidate_answers(summary: str):
    return sum((get_ngrams(clean_text(summary), j) for j in range(1, 4)), [])


def ngram_score(ngram) -> int:
    return 3 ** sum(1 for word in ngram if word == word.capitalize())


def get_candidate_answers(summaries):
    answer_scores = defaultdict(int)
    for summary in summaries:
        for ngram in candidate_answers(summary):
            answer_scores[ngram] += ngram_score(ngram)
    return sorted(answer_scores.items(), key=lambda x: x[1], reverse=True)


def answer_ranking(summaries, num=10):
    answers = get_candidate_answers(summaries)
    for i, (answer, score) in enumerate(answers, start=1):
        print(i, answer, f"({score})")
        if i == 10:
            break


def rewrite_query(query):
    query = clean_text(query)
    return " ".join(word for word in query.split(" ") if word.lower() not in stopwords)
