# src/research_paper_ai/tests/test_research_planning.py

from research_paper_ai.models.paper_brief import (
    PaperBrief
)

from research_paper_ai.crews.research_planning_crew import (
    run_research_planning
)

from research_paper_ai.parsers.research_plan_parser import (
    ResearchPlanParser
)


paper_brief = PaperBrief(
    topic="AI for Lung Cancer Detection",
    domain="Healthcare AI",
    paper_type="Research Paper",
    objectives=[
        "Improve diagnostic accuracy",
        "Reduce false positives"
    ],
    keywords=[
        "AI",
        "Lung Cancer",
        "Deep Learning"
    ]
)

raw_output = run_research_planning(
    paper_brief
)

research_plan = ResearchPlanParser.parse(
    str(raw_output)
)

print("\n===== RESEARCH PLAN =====\n")

print("TITLE:")
print(research_plan.title)

print("\nOUTLINE:")
for item in research_plan.outline:
    print("-", item)

print("\nRESEARCH QUESTIONS:")
for item in research_plan.research_questions:
    print("-", item)

print("\nLITERATURE REQUIREMENTS:")
for item in research_plan.literature_requirements:
    print("-", item)

print("\nRESEARCH PLANNING TEST PASSED")