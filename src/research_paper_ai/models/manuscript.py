from dataclasses import dataclass


@dataclass
class Manuscript:
    title: str = ""
    content: str = ""