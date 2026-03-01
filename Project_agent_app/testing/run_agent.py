from agent.graph import app_graph

def main():
    print("\nEnterprise HR Policy Assistant (type 'exit' to quit)\n")

    # Initial state
    state = {
        "query": "",
        "name": None,
        "designation": None,
        "lead_capture_complete": False,
        "conversation_end": False,
        "response": ""
    }

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        # Exit if user types exit
        if user_input.lower() in ["exit", "quit"]:
            print(f"Agent: Goodbye, {state.get('name', 'User')}! 👋")
            break

        # Update state
        state["query"] = user_input

        # Run LangGraph
        state = app_graph.invoke(state)

        # Print agent response
        print(f"Agent: {state.get('response', '')}")
        print("-" * 50)

        # Exit if graph signals end
        if state.get("conversation_end", False):
            break


if __name__ == "__main__":
    main()