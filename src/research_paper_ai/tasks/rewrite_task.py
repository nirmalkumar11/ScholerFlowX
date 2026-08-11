from crewai import Task


def create_rewrite_task(
    agent,
    manuscript_text,
    review_report
):

    comments = "\n".join(
        f"- {c}"
        for c in review_report.comments
    )

    return Task(
        description=f"""
Rewrite the manuscript.

Fix every issue listed below.

REVIEW COMMENTS:

{comments}

RULES:

Remove all forbidden content.

Do not introduce new facts.

Return the revised manuscript only.

MANUSCRIPT:

{manuscript_text}
""",
        expected_output=(
            "Revised manuscript"
        ),
        agent=agent
    )