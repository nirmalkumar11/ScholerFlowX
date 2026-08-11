# src/research_paper_ai/tests/test_paper_brief_parser.py

from research_paper_ai.parsers.paper_brief_parser import (
    PaperBriefParser
)

sample_output = """
{
  "topic": "AI for Lung Cancer Detection",
  "domain": "Healthcare AI",
  "paper_type": "Research Paper",
  "objectives": [
    "Improve diagnostic accuracy",
    "Reduce false positives"
  ],
  "keywords": [
    "AI",
    "Lung Cancer",
    "Deep Learning"
  ],
  "constraints": []
}
"""

paper_brief = PaperBriefParser.parse(
sample_output
)

print("\n=== PAPER BRIEF ===\n")

print("Topic:", paper_brief.topic)
print("Domain:", paper_brief.domain)
print("Paper Type:", paper_brief.paper_type)
print("Objectives:", paper_brief.objectives)
print("Keywords:", paper_brief.keywords)

print("\nPARSER TEST PASSED")


