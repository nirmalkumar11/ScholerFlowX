from crewai import Agent

from research_paper_ai.llm.groq_llm import get_llm


def create_literature_ranking_agent():
    return Agent(
        role="Literature Ranking Specialist",
        goal="Rank retrieved papers by relevance.",
        backstory=(
            "You are an academic reviewer who identifies "
            "the most relevant papers for a research project."
        ),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )