from crewai import Agent, Task, Crew, LLM

llm = LLM(
    model="ollama/qwen2.5-coder:3b",
    base_url="http://localhost:11434"
)

agent = Agent(
    role="Tester",
    goal="Respond with exactly CREWAI_OLLAMA_OK",
    backstory="You are a testing agent.",
    llm=llm,
    verbose=True
)

task = Task(
    description="Reply with exactly CREWAI_OLLAMA_OK",
    expected_output="CREWAI_OLLAMA_OK",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()

print("\nRESULT:")
print(result)