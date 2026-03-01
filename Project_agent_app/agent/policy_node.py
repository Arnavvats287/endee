from agent.rag_tool import rag_search

def policy_node(state):
    query = state["query"]

    result = rag_search(query)

    # Store full RAG output in state
    state["top_matches"] = result["top_matches"]
    state["answer"] = result["answer"]

    state["response"] = result["answer"]
    state["response"] += "\n\nWould you like to ask another question? (yes/no)"

    return state