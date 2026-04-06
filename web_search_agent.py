from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.duckduckgo import DuckDuckGoTools

# Define the agent
search_agent = Agent(
    name="Web Search Agent",
    model=Claude(id="claude-sonnet-4-5"),
    db=SqliteDb(db_file="agent_sessions.db"),
    tools=[DuckDuckGoTools()],
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
)

# Serve as production API with AgentOS
agent_os = AgentOS(agents=[search_agent], tracing=True)
app = agent_os.get_app()
