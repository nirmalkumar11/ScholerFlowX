# src/research_paper_ai/services/citation_service.py

from research_paper_ai.models.citation_package import (
    CitationPackage
)

from research_paper_ai.tools.citation_tool import (
    CitationTool
)


def create_citation_package(
    papers
):
    bibtex = CitationTool.generate_bibtex(
        papers
    )

    return CitationPackage(
        bibtex_content=bibtex
    )