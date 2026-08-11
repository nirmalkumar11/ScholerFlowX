from dataclasses import dataclass, field


@dataclass
class Paper:
    title: str = ""
    authors: list[str] = field(default_factory=list)
    summary: str = ""
    published: str = ""
    arxiv_url: str = ""


@dataclass
class LiteratureCorpus:
    papers: list[Paper] = field(default_factory=list)