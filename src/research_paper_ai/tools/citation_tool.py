# src/research_paper_ai/tools/citation_tool.py

class CitationTool:

    @staticmethod
    def generate_bibtex(papers):

        entries = []

        for idx, paper in enumerate(
            papers,
            start=1
        ):

            year = ""

            if paper.published:
                year = paper.published[:4]

            authors = " and ".join(
                paper.authors
            )

            bibtex = f"""
@article{{paper{idx},
  title={{ {paper.title} }},
  author={{ {authors} }},
  year={{ {year} }},
  url={{ {paper.arxiv_url} }}
}}
"""

            entries.append(
                bibtex.strip()
            )

        return "\n\n".join(entries)