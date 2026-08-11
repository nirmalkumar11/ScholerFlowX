from research_paper_ai.models.research_plan import (
    ResearchPlan
)

from research_paper_ai.crews.literature_retrieval_crew import (
    run_literature_retrieval
)


research_plan = ResearchPlan(
    title="Comparing Deep Learning Models for Lung Cancer Detection Using AI",
    research_questions=[
        "What is the comparative performance of deep learning algorithms for lung cancer detection?"
    ]
)

corpus = run_literature_retrieval(
    research_plan
)

print("\n===== LITERATURE CORPUS =====\n")

print(
    f"Retrieved {len(corpus.papers)} papers\n"
)

for idx, paper in enumerate(
    corpus.papers,
    start=1
):
    print(f"\nPaper {idx}")
    print("Title:", paper.title)
    print("Authors:", ", ".join(paper.authors))
    print("Published:", paper.published)
    print("URL:", paper.arxiv_url)

print(
    "\nLITERATURE RETRIEVAL TEST PASSED"
)