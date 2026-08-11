from research_paper_ai.models.literature_corpus import (
    Paper
)

from research_paper_ai.models.ranked_paper import (
    RankedPaper
)

from research_paper_ai.utils.ranking_utils import (
    get_top_papers
)


paper_a = Paper(
    title="Paper A"
)

paper_b = Paper(
    title="Paper B"
)

paper_c = Paper(
    title="Paper C"
)

rankings = [
    {
        "paper": paper_a,
        "ranked": RankedPaper(
            title="Paper A",
            score=70,
            reason="test"
        )
    },
    {
        "paper": paper_b,
        "ranked": RankedPaper(
            title="Paper B",
            score=95,
            reason="test"
        )
    },
    {
        "paper": paper_c,
        "ranked": RankedPaper(
            title="Paper C",
            score=85,
            reason="test"
        )
    }
]

top_papers = get_top_papers(
    rankings,
    top_k=3
)

print("\n===== TOP PAPERS =====\n")

for paper in top_papers:
    print(paper.title)

print("\nTOP PAPER TEST PASSED")