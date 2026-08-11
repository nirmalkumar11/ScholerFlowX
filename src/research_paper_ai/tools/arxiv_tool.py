import time
import requests
import xml.etree.ElementTree as ET

from research_paper_ai.models.literature_corpus import (
    Paper
)


class ArxivTool:

    BASE_URL = "https://export.arxiv.org/api/query"

    @staticmethod
    def search(
        query: str,
        max_results: int = 5
    ):
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results
        }

        response = None

        for attempt in range(3):

            try:

                response = requests.get(
                    ArxivTool.BASE_URL,
                    params=params,
                    timeout=30,
                    headers={
                        "User-Agent":
                        "ResearchPaperAI/1.0"
                    }
                )

                response.raise_for_status()

                break

            except requests.exceptions.HTTPError:

                if (
                    response is not None
                    and response.status_code == 429
                ):
                    print(
                        f"Rate limited. Retry {attempt + 1}/3"
                    )

                    time.sleep(5)

                else:
                    raise

        else:
            raise Exception(
                "Arxiv API rate limit exceeded."
            )

        root = ET.fromstring(
            response.text
        )

        ns = {
            "atom": "http://www.w3.org/2005/Atom"
        }

        papers = []

        for entry in root.findall(
            "atom:entry",
            ns
        ):
            title = entry.find(
                "atom:title",
                ns
            ).text.strip()

            summary = entry.find(
                "atom:summary",
                ns
            ).text.strip()

            published = entry.find(
                "atom:published",
                ns
            ).text.strip()

            link = entry.find(
                "atom:id",
                ns
            ).text.strip()

            authors = []

            for author in entry.findall(
                "atom:author",
                ns
            ):
                authors.append(
                    author.find(
                        "atom:name",
                        ns
                    ).text.strip()
                )

            papers.append(
                Paper(
                    title=title,
                    authors=authors,
                    summary=summary,
                    published=published,
                    arxiv_url=link
                )
            )

        print("\n===== ARXIV DEBUG =====")
        print("Query:", query)
        print("Papers Found:", len(papers))
        print("=======================\n")

        return papers