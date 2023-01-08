from text_generator import HMMGenerator
from util import SimpleAncoraCorpusReader


def show_ngram_title(n: int = 1) -> str:
    print("=" * 79)
    print(f"Oraciones con ngramas n = {n}")
    print("=" * 79)


# $("main").querySelectorAll("p")[0].textContent
def main():
    ANCORA_CORPUS_DIR = "resources/ancora-3.0.1es"
    corpus_reader = SimpleAncoraCorpusReader(str(ANCORA_CORPUS_DIR))

    # TODO: Add to tests
    # hmm.train([["Hello", "world", "!"]])
    sents = corpus_reader.sents()
    hmm = HMMGenerator(2)
    hmm.train(sents)

    show_ngram_title(2)
    for _ in range(10):
        print(hmm.generate_random_sentence())

    sents = corpus_reader.sents()
    hmm = HMMGenerator(3)
    hmm.train(sents)
    show_ngram_title(3)
    for _ in range(10):
        print(hmm.generate_random_sentence())

    sents = corpus_reader.sents()
    hmm = HMMGenerator(5)
    hmm.train(sents)
    show_ngram_title(5)
    for _ in range(10):
        print(hmm.generate_random_sentence())


if __name__ == "__main__":
    main()
