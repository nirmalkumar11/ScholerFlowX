from crewai import Task

from research_paper_ai.models.paper_brief import PaperBrief


def create_research_planning_task(
    agent,
    paper_brief: PaperBrief
):
    return Task(
        description=f"""
Create a research plan based on the following paper brief.

Topic:
{paper_brief.topic}

Domain:
{paper_brief.domain}

Objectives:
{paper_brief.objectives}

Keywords:
{paper_brief.keywords}

Generate:

1. Research Title
2. Paper Outline
3. Research Questions
4. Literature Requirements

Return ONLY valid JSON.
""",


expected_output="""
Return the answer using EXACTLY this structure:

{
  "Title": "...",

  "Outline":
   - item 1
   - item 2
   - item 3

  "Research Questions":
   - question 1
   - question 2

  "Literature Requirements":
   - requirement 1
   - requirement 2
}

Keep the same headings exactly.
"""
,
        agent=agent
    )