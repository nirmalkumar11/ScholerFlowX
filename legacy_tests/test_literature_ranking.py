from research_paper_ai.models.research_plan import (
    ResearchPlan
)

from research_paper_ai.crews.literature_retrieval_crew import (
    run_literature_retrieval
)

from research_paper_ai.crews.literature_ranking_crew import (
    run_literature_ranking
)

from research_paper_ai.parsers.literature_ranking_parser import (
    LiteratureRankingParser
)


plan = ResearchPlan(
    title="Deep Learning for Lung Cancer Detection"
)

corpus = run_literature_retrieval(
    plan
)

raw_output = run_literature_ranking(
    research_topic=plan.title,
    papers=corpus.papers
)

rankings = LiteratureRankingParser.parse(
    raw_output,
    corpus.papers
)

print("\n===== RANKED PAPERS =====\n")

for idx, item in enumerate(rankings, start=1):

    print(f"Rank {idx}")

    print(
        "Score:",
        item["ranked"].score
    )

    print(
        "Title:",
        item["paper"].title
    )

    print(
        "Reason:",
        item["ranked"].reason
    )

    print()

print(
    "LITERATURE RANKING TEST PASSED"
)