from langgraph.graph import StateGraph, START, END
from backend.graph.state import AgentState

from backend.agents.orchestrator_agent import orchestrator_agent
from backend.agents.visual_agent import visual_analysis_agent
from backend.agents.speech_agent import speech_agent
from backend.tools.mcp_tools import describe_image_tool


builder = StateGraph(AgentState)


# nodes
builder.add_node("orchestrator", orchestrator_agent)


def vision_node(state):
    return describe_image_tool(visual_analysis_agent, state)


builder.add_node("vision", vision_node)
builder.add_node("speech", speech_agent)


# flow
builder.add_edge(START, "orchestrator")


def route(state):
    if state.get("valid_image") is False:
        return END
    return "vision"


builder.add_conditional_edges("orchestrator", route)

builder.add_edge("vision", "speech")
builder.add_edge("speech", END)


workflow = builder.compile()