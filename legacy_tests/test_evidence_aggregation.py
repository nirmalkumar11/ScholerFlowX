from research_paper_ai.crews.evidence_extraction_crew import (
    run_evidence_extraction
)

from research_paper_ai.models.literature_corpus import (
    Paper
)

papers = [
    Paper(
        title="Paper 1",
        summary="""
        Deep CNN

        Dataset:
        LC25000

        Accuracy:
        99%
        """
    ),
    Paper(
        title="Paper 2",
        summary="""
        Ensemble Learning

        Dataset:
        CT Scan Dataset

        Accuracy:
        95%
        """
    )
]

package = (
    run_evidence_extraction(
        papers
    )
)

print("\n===== EVIDENCE PACKAGE =====\n")

for item in package.evidence_items:

    print(item)