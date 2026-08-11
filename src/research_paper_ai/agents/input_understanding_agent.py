from crewai import Agent

from research_paper_ai.llm.groq_llm import get_llm


def create_input_understanding_agent():
    return Agent(
        role="Research Understanding Specialist",
        goal=(
            "Analyze research materials and identify "
            "research domain, objectives, keywords, "
            "constraints and paper requirements."
        ),
        backstory=(
            "You are a senior academic research analyst. "
            "You transform raw research documents into "
            "structured research briefs."
        ),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )