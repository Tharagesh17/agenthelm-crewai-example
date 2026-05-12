import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# Load environment variables
load_dotenv()

# Import AgentHelm
from agenthelm import agenthelm

# ====================== AGENTHELM WRAPPER ======================
@agenthelm.wrap(
    budget=25.0,                    # Max $25 budget for this agent
    telegram_control=True,          # Enable Telegram human-in-the-loop
    fail_closed=True,               # Stop everything if safety/budget breached
    checkpointing=True,             # Auto-save state
)
class ResearchAgent(Agent):
    """Example agent wrapped with AgentHelm governance"""
    def __init__(self):
        super().__init__(
            role="Senior Research Analyst",
            goal="Research any topic thoroughly and give accurate summaries",
            backstory="You are an expert researcher who works with full transparency and safety.",
            verbose=True,
            allow_delegation=False,
            max_iter=10
        )

# ====================== CREWAI SETUP ======================
if __name__ == "__main__":
    print("🚀 Starting CrewAI agent with AgentHelm governance...\n")

    researcher = ResearchAgent()

    task = Task(
        description="Research the latest features of Grok 4 by xAI and give a clear summary.",
        expected_output="A well-structured bullet point summary with key points",
        agent=researcher
    )

    crew = Crew(
        agents=[researcher],
        tasks=[task],
        verbose=2,
        memory=True
    )

    result = crew.kickoff()

    print("\n" + "="*60)
    print("✅ FINAL RESULT:")
    print(result)
    print("="*60)
    print("\n🔍 Check your AgentHelm dashboard: https://agenthelm.online/dashboard")
