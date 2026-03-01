from langgraph.graph import StateGraph
from agent.intent_chain import detect_intent
from agent.lead_capture_node import lead_capture_node
from agent.policy_node import policy_node

def router(state):
    last_input = state.get("query", "").strip().lower()
# full ghraph logic
    # Lead capture not done yet
    if not state.get("lead_capture_complete", False):
        return lead_capture_node(state)

    # User wants to exit
    if last_input in ["no", "exit", "quit"]:
        state["response"] = f"Goodbye, {state.get('name', 'User')}! 👋"
        state["conversation_end"] = True
        return state

    # User wants to continue querying policies
    if last_input in ["yes", "y"]:
        state["response"] = "Great! What company policy would you like to know?"
        return state

    # Normal intent detection
    intent = detect_intent(state["query"])
    if intent == "lead_capture":
        return lead_capture_node(state)
    else:
        return policy_node(state)

# Initialize graph
graph = StateGraph(dict)
graph.add_node("router", router)
graph.set_entry_point("router")
graph.set_finish_point("router")
app_graph = graph.compile()