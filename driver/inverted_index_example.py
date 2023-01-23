from pathlib import Path
from ir import InMemoryInvertedIndex, LemmaTokenizer

RESOURCE_PATH = Path("./resources")


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
    tokenizer = LemmaTokenizer.load_from_file(RESOURCE_PATH / "lemmatization-es.txt")
    docs = []
    for path in (RESOURCE_PATH / "documents").glob("*.txt"):
        with open(path, "r") as doc:
            docs.append(doc.read())

    inverted_index = InMemoryInvertedIndex(docs, tokenizer)
    while True:
        query = input("Ingresar búsqueda: ")
        results = inverted_index.search(query)
        print(results)
        query = input("Mostrar texto? (S/s)")
        if query.lower().strip() == "s":
            for i, result in enumerate(results, start=1):
                print("=" * 79)
                print(f"Resultado {i}")
                print("=" * 79)
                print(docs[result])
