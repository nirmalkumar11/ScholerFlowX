from crewai import Agent

from research_paper_ai.llm.groq_llm import get_llm


def create_evidence_extraction_agent():
    return Agent(
        role="Research Evidence Extractor",
        goal=(
            "Extract methodologies, datasets "
            "and results exactly as reported."
        ),
        backstory=(
            "Expert systematic literature reviewer."
        ),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )