import re

def lead_capture_node(state):
    query = state["query"]

    # Regex
    match = re.search(r"(?:my name is|i am)\s+([A-Za-z]+(?: [A-Za-z]+)?)\s*,?\s*(?:am a |as a |, )?\s*([A-Za-z]+)", query, re.IGNORECASE)
    if match:
        name = match.group(1).strip().title()
        designation = match.group(2).strip().title()

        state["name"] = name
        state["designation"] = designation
        state["lead_capture_complete"] = True

        state["response"] = (
            f"Hi {name}, {designation}! 🎉\n\n"
            "You are now registered.\n"
            "What company policy would you like to know?"
        )
        return state

    # ask again
    state["response"] = (
        "Hello! 👋 Welcome to the Enterprise HR Policy Assistant.\n\n"
        "Please tell me your name and designation to continue (e.g., 'My name is Arnav, Manager')."
    )
    return state