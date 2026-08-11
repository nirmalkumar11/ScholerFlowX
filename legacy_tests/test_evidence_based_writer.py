from research_paper_ai.models.paper_brief import (
    PaperBrief
)

from research_paper_ai.models.research_plan import (
    ResearchPlan
)

from research_paper_ai.models.citation_package import (
    CitationPackage
)

from research_paper_ai.models.evidence_package import (
    EvidenceItem,
    EvidencePackage
)

from research_paper_ai.crews.paper_writing_crew import (
    run_paper_writer
)

paper_brief = PaperBrief(
    topic="AI for Lung Cancer Detection"
)

research_plan = ResearchPlan(
    title="AI for Lung Cancer Detection"
)

citations = CitationPackage(
    bibtex_content="""
@article{paper1}
"""
)

evidence_package = EvidencePackage(
    evidence_items=[
        EvidenceItem(
            paper_title="Paper 1",
            methodologies=[
                "Deep CNN"
            ],
            datasets=[
                "LC25000"
            ],
            results=[
                "Accuracy: 99%"
            ]
        ),
        EvidenceItem(
            paper_title="Paper 2",
            methodologies=[
                "Ensemble Learning"
            ],
            datasets=[
                "CT Scan Dataset"
            ],
            results=[
                "Accuracy: 95%"
            ]
        )
    ]
)

manuscript = run_paper_writer(
    paper_brief,
    research_plan,
    evidence_package,
    citations
)

print(
    manuscript.content[:3000]
)