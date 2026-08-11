from crewai import Agent

from research_paper_ai.llm.groq_llm import get_llm


def create_research_planning_agent():
    return Agent(
        role="Research Planning Specialist",
        goal=(
            "Create a detailed research plan "
            "for an academic paper."
        ),
        backstory=(
            "You are an experienced academic researcher "
            "who designs publication-quality research plans."
        ),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )