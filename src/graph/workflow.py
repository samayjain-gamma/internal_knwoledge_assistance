from langgraph.graph import END, StateGraph

from src.graph.nodes import (
    check_exit,
    detect_injection,
    detect_injection_check,
    exit_router,
    generate_answer,
    get_user_input,
    input_validation_check,
    retrieve_docs,
    rewrite_query,
    update_history,
    validate_input,
)
from src.graph.state import GraphState
from src.monitoring.metrics import start_metrics_server


def build_graph():
    """
    Thsi is the entry point for Chat
    """

    builder = StateGraph(GraphState)

    builder.add_node("get_input", get_user_input)
    builder.add_node("check_exit", check_exit)
    builder.add_node("validate_input", validate_input)
    builder.add_node("detect_injection", detect_injection)
    builder.add_node("rewrite_query", rewrite_query)
    builder.add_node("retrieve_docs", retrieve_docs)
    builder.add_node("generate_answer", generate_answer)
    builder.add_node("update_history", update_history)

    builder.set_entry_point("get_input")
    builder.add_edge("get_input", "check_exit")

    builder.add_conditional_edges(
        "check_exit", exit_router, {True: END, False: "validate_input"}
    )

    builder.add_conditional_edges(
        "validate_input", input_validation_check, {True: "detect_injection", False: END}
    )

    builder.add_conditional_edges(
        "detect_injection",
        detect_injection_check,
        {
            True: END,
            False: "rewrite_query",
        },
    )

    builder.add_edge("rewrite_query", "retrieve_docs")
    builder.add_edge("retrieve_docs", "generate_answer")
    builder.add_edge("generate_answer", "update_history")
    builder.add_edge("update_history", "get_input")

    return builder.compile()


if __name__ == "__main__":

    start_metrics_server()
    graph = build_graph()

    graph.invoke({})
