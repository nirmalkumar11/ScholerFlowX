from crewai import Crew

from research_paper_ai.agents.evidence_extraction_agent import (
    create_evidence_extraction_agent
)

from research_paper_ai.tasks.evidence_extraction_task import (
    create_evidence_extraction_task
)

from research_paper_ai.parsers.evidence_parser import (
    EvidenceParser
)

paper_title = (
    "Machine Learning-based Lung and "
    "Colon Cancer Detection"
)

paper_summary = """
Hybrid ensemble feature extraction model.

Deep feature extraction.

Ensemble learning.

Evaluated on LC25000 dataset.

Accuracy:
99.05%
100%
99.30%
"""

agent = create_evidence_extraction_agent()

task = create_evidence_extraction_task(
    agent,
    paper_title,
    paper_summary
)

crew = Crew(
    agents=[agent],
    tasks=[task]
)

result = crew.kickoff()

evidence = (
    EvidenceParser.parse(result)
)

print("\n===== EVIDENCE =====\n")
print(evidence)