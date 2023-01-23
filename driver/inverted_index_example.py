from pathlib import Path
from ir import InMemoryInvertedIndex, LemmaTokenizer

if __name__ == "__main__":
    tokenizer = LemmaTokenizer({})
    docs = [
        "new home sales top forecast",
        "home sales rise in july",
        "increase in home sales in july",
        "july new home sales rise",
    ]

    inverted_index = InMemoryInvertedIndex(docs, tokenizer)
    print(inverted_index._terms)
    print(inverted_index.search("july sales rise"))
    tokenizer = LemmaTokenizer.load_from_file(Path("./lemmatization-es.txt"))
    docs = []
    for path in Path("./documents").glob("*.txt"):
        with open(path, "r") as doc:
            docs.append(doc.read())

    inverted_index = InMemoryInvertedIndex(docs, tokenizer)
    query = input("Ingresar búsqueda: ")
    print(inverted_index.search(query))
