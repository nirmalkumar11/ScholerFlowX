from crewai import Agent

from research_paper_ai.llm.groq_llm import (
    get_llm
)


def create_rewrite_agent():
    return Agent(
        role="Academic Manuscript Rewriter",
        goal=(
            "Revise a manuscript based on "
            "review comments."
        ),
        backstory=(
            "Expert journal editor."
        ),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )