import streamlit as st
import time

def stream_response(response):
    """Streaming LLM Response for smoothier experience."""
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.02)

def display_history():
    """Displaying the chat history in the reverse order."""
    history_container = st.container()

    with history_container: 
        if st.session_state["history"]:
            for index, entry in enumerate(reversed(st.session_state["history"])):
                if index == 0:
                    st.markdown(f"## You: {entry['query']}")
                    st.write_stream(stream_response(entry["response"]))
                    st.markdown("------------") 
                else:
                    st.markdown(f"## You: {entry['query']}")
                    st.markdown(f"## Assistant:\n{entry['response']}")
                    st.markdown("------------") 