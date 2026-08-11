
from crewai import LLM

def get_llm():
    return LLM(
        model="ollama/mistral:7b",
        base_url="http://localhost:11434",
        temperature=0.1
    )