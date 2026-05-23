from langgraph.graph import StateGraph
from langgraph.graph import START, END

from graph.state import AgentState

from agents.orchestrator_agent import orchestrator_agent
from agents.visual_agent import visual_analysis_agent
from agents.speech_agent import speech_agent


builder = StateGraph(AgentState)

builder.add_node(
    "orchestrator",
    orchestrator_agent
)

builder.add_node(
    "visual_agent",
    visual_analysis_agent
)

builder.add_node(
    "speech_agent",
    speech_agent
)

builder.add_edge(
    START,
    "orchestrator"
)

builder.add_edge(
    "orchestrator",
    "visual_agent"
)

builder.add_edge(
    "visual_agent",
    "speech_agent"
)

builder.add_edge(
    "speech_agent",
    END
)

workflow = builder.compile()