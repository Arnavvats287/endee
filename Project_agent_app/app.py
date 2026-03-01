# streamlit app.py

import streamlit as st
import json
from agent.graph import app_graph

st.set_page_config(page_title="Enterprise HR Assistant", page_icon="💼")

st.title("💼 Enterprise HR Policy Assistant")

# Session state initialization 
if "state" not in st.session_state:
    st.session_state.state = {
        "query": "",
        "name": None,
        "designation": None,
        "lead_capture_complete": False,
        "conversation_end": False,
        "response": ""
    }

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_rag_result" not in st.session_state:
    st.session_state.last_rag_result = None

# User info 
if st.session_state.state.get("name"):
    st.markdown(f"👤 **User:** {st.session_state.state.get('name')} | **Role:** {st.session_state.state.get('designation', 'N/A')}")

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

#  Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to history
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Exit 
    if user_input.lower() in ["exit", "quit"]:
        goodbye = f"Goodbye, {st.session_state.state.get('name', 'User')}! 👋"
        st.session_state.chat_history.append(("assistant", goodbye))
        with st.chat_message("assistant"):
            st.markdown(goodbye)
        st.stop()

    # Update 
    st.session_state.state["query"] = user_input

    #  Agent response 
    with st.spinner("Thinking... 🤔"):
        state = app_graph.invoke(st.session_state.state)
        st.session_state.state = state

    response = state.get("response", "")

    # Add assistant message to history
    st.session_state.chat_history.append(("assistant", response))
    with st.chat_message("assistant"):
        st.markdown(response)

    # Show RAG details 
    if "top_matches" in state and state.get("top_matches"):
        with st.expander("🔎 View detailed retrieved context & similarity scores"):
            for i, match in enumerate(state["top_matches"], 1):
                st.markdown(f"**Match {i}**")
                st.write(match["text"])
                st.write(f"Similarity Score: `{match['similarity']:.4f}`")
                st.divider()

        # JSON download button
        json_data = json.dumps({
            "query": state.get("query"),
            "top_matches": state.get("top_matches"),
            "answer": state.get("answer")
        }, indent=4)

        st.download_button(
            label="⬇️ Download RAG Result as JSON",
            data=json_data,
            file_name="rag_result.json",
            mime="application/json"
        )
