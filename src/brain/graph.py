from langgraph.graph import StateGraph, END
from src.brain.state import CognitiveState
from src.brain.nodes import (
    classify_input_node,
    emotional_validation_node,
    uncertainty_arbiter_node,
    response_synthesizer_node,
)

def route_after_classification(state: CognitiveState) -> str:
    emotion = state.get("detected_emotion", "neutral")
    if emotion in ["lonely", "distress"]:
        return "validator"
    elif state.get("requires_grounding", False):
        return "arbiter"
    return "synthesizer"

def build_cognitive_graph():
    workflow = StateGraph(CognitiveState)

    # Register nodes
    workflow.add_node("classifier", classify_input_node)
    workflow.add_node("validator", emotional_validation_node)
    workflow.add_node("arbiter", uncertainty_arbiter_node)
    workflow.add_node("synthesizer", response_synthesizer_node)

    # Define entry point
    workflow.set_entry_point("classifier")

    # Conditional routing based on emotional state and grounding flags
    workflow.add_conditional_edges(
        "classifier",
        route_after_classification,
        {
            "validator": "validator",
            "arbiter": "arbiter",
            "synthesizer": "synthesizer",
        },
    )

    # Convergence edges
    workflow.add_edge("validator", "synthesizer")
    workflow.add_edge("arbiter", "synthesizer")
    workflow.add_edge("synthesizer", END)

    return workflow.compile()

cognitive_app = build_cognitive_graph()