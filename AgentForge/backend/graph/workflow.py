from langgraph.graph import StateGraph, START, END

from backend.graph.state import AgentState

from backend.agents.orchestrator_agent import orchestrator_agent
from backend.agents.visual_agent import visual_analysis_agent
from backend.agents.speech_agent import speech_agent


builder = StateGraph(AgentState)


# nodes
builder.add_node("orchestrator", orchestrator_agent)
builder.add_node("visual_agent", visual_analysis_agent)
builder.add_node("speech_agent", speech_agent)


# entry
builder.add_edge(START, "orchestrator")


def route_after_orchestrator(state):
    if state.get("valid_image") is False:
        return END
    return "visual_agent"


builder.add_conditional_edges(
    "orchestrator",
    route_after_orchestrator
)


# normal flow
builder.add_edge("visual_agent", "speech_agent")
builder.add_edge("speech_agent", END)


workflow = builder.compile()