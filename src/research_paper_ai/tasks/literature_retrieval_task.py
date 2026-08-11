from crewai import Task

from research_paper_ai.models.research_plan import (
    ResearchPlan
)


def create_literature_retrieval_task(
    agent,
    research_plan: ResearchPlan
):
    return Task(
        description=f"""
Research Title:
{research_plan.title}

Research Questions:
{research_plan.research_questions}

Generate ONE concise academic search query.

Requirements:
- Maximum 10 words
- Focus on core concepts
- Return ONLY the query text
""",
        expected_output="A search query string",
        agent=agent
    )