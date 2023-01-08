from bs4 import BeautifulSoup
import requests
from ask_msr import answer_ranking, rewrite_query


if __name__ == "__main__":
    while True:
        query = input()

        rewritten_query = rewrite_query(query)

        params = {"q": rewritten_query, "setLang": "es"}

        headers = {"User-agent": "Mozilla/11.0"}

        res = requests.get(
            "https://www.bing.com/search", params=params, headers=headers
        )

        soup = BeautifulSoup(res.text, "html.parser")
        summaries = [p.get_text() for p in soup.find_all("p")]

        answer_ranking(summaries)
