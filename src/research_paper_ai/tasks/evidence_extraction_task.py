from crewai import Task


def create_evidence_extraction_task(
    agent,
    paper_title,
    paper_summary
):
    description = f"""
Extract evidence ONLY from the paper.

Return exactly:

TITLE:
<paper title>

METHODOLOGIES:
- item
- item

DATASETS:
- item

RESULTS:
- item

RULES:

Do not summarize.

Do not infer.

Do not invent.

Only extract information
explicitly stated.

PAPER TITLE:
{paper_title}

PAPER SUMMARY:
{paper_summary}
"""

    return Task(
        description=description,
        expected_output="Structured evidence",
        agent=agent
    )