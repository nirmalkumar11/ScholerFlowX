from crewai import Task


def create_literature_ranking_task(
    agent,
    research_topic,
    papers
):
    papers_text = ""

    for idx, paper in enumerate(papers, start=1):
        papers_text += f"""
Paper {idx}
Title: {paper.title}
Summary: {paper.summary}

"""

    return Task(
        description=f"""
Research Topic:
{research_topic}

Rank the following papers by relevance.

{papers_text}

Return EXACTLY this format:

1|score|reason
2|score|reason
3|score|reason
...

Score must be between 1 and 100.
""",
        expected_output="""
1|95|Highly relevant
2|88|Relevant
3|75|Somewhat relevant
""",
        agent=agent
    )