from dataclasses import dataclass


@dataclass
class RankedPaper:
    title: str
    score: int
    reason: str