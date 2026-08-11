from research_paper_ai.models.paper_brief import (
    PaperBrief
)

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

from research_paper_ai.utils.ranking_utils import (
    get_top_papers
)

from research_paper_ai.services.citation_service import (
    create_citation_package
)

from research_paper_ai.crews.paper_writing_crew import (
    run_paper_writer
)


paper_brief = PaperBrief(
    topic="Deep Learning for Lung Cancer Detection",
    domain="Healthcare AI",
    objectives=[
        "Improve diagnostic accuracy",
        "Reduce false positives"
    ]
)

research_plan = ResearchPlan(
    title="Deep Learning for Lung Cancer Detection",
    research_questions=[
        "How can deep learning improve lung cancer detection?"
    ],
    raw_plan="""
Introduction
Literature Review
Methodology
Results
Discussion
Conclusion
"""
)

corpus = run_literature_retrieval(
    research_plan
)

print("\n===== RETRIEVAL DEBUG =====")

print("Corpus:", corpus)

if corpus:
    print("Papers:", corpus.papers)

    if corpus.papers:
        print("Paper Count:", len(corpus.papers))

print("===========================\n")

raw_ranking = run_literature_ranking(
    research_topic=paper_brief.topic,
    papers=corpus.papers
)

rankings = LiteratureRankingParser.parse(
    raw_ranking,
    corpus.papers
)

top_papers = get_top_papers(
    rankings,
    top_k=3
)

citation_package = create_citation_package(
    top_papers
)

manuscript = run_paper_writer(
    paper_brief,
    research_plan,
    top_papers,
    citation_package
)

print("\n===== SAFE MANUSCRIPT =====\n")

print(manuscript.content[:5000])

print("\nSAFE PAPER WRITER TEST PASSED")