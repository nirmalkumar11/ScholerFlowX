# src/research_paper_ai/models/research_package.py

from dataclasses import dataclass, field


@dataclass
class ResearchPackage:
    raw_text: str = ""

    documents: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    diagrams: list[str] = field(default_factory=list)
    datasets: list[str] = field(default_factory=list)

    requirements: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)