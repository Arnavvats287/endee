from agent.graph import app_graph
from agent.state import AgentState

def test_langgraph(query):
    state = AgentState({"query": query})
    final_state = app_graph.invoke(state)
    print("Query:", query)
    print("Response:", final_state.get("response", ""))

if __name__ == "__main__":
    # Lead capture test
    test_langgraph("My name is Alice, Manager")
    
    # Policy query test
    test_langgraph("How will employees be notified about major policy changes?")