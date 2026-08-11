from crewai import Task


def create_input_understanding_task(
    agent,
    research_text: str
):
    return Task(
        description=f"""
Analyze the following research content.

Research Content:
{research_text}

Extract:

1. Main Topic
2. Research Domain
3. Paper Type
4. Research Objectives
5. Keywords
6. Constraints

Return the result in JSON format.
""",
        expected_output="""
Valid JSON with:

topic
domain
paper_type
objectives
keywords
constraints
""",
        agent=agent
    )
