import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.llm.ollama_client import OllamaClient
from src.retrieval.search_engine import SearchEngine

def initialize_session_state():
    """Initiliazing session state."""
    if "llm_client" not in st.session_state:
        st.session_state["llm_client"] = OllamaClient(model_name="llama3.1")
        st.session_state["search_engine"] = SearchEngine()
    if "query" not in st.session_state:
        st.session_state["query"] = ""
    if "history" not in st.session_state:
        st.session_state["history"] = []

def main():
    st.title("Documentation Search Assistant")
    st.write("""Ask questions about Python or Django.""")

    # Initiliazing the components
    initialize_session_state()
    llm_client = st.session_state["llm_client"]
    search_engine = st.session_state["search_engine"]
    
    query = st.text_input("Input query: ", value=st.session_state["query"], key="query")

    if st.session_state["history"]:
        for entry in st.session_state["history"]:
            st.markdown(f"You: {entry['query']}")
            st.markdown(f"Assistant: {entry['response']}")
            st.markdown("------------") 

    if st.button("Search"):
        if query:
            try:
                with st.spinner("Generating response: "):
                    search_results = search_engine.search(query)
                    response = llm_client.generate_response(query, search_results)
                
                st.session_state.history.append({
                    "query": query,
                    "response": response["llm_response"]
                })
                
                st.session_state.query = ""
            
            except Exception as e:
                st.error("An error occurred while processing your request!")
        
        else:
            st.error("Please enter your request!")    
    
    if st.session_state["history"]:
        result = st.session_state["history"][-1]
        st.markdown(f"You: {result['query']}")
        st.markdown(f"Assistant: {result['response']}")
        # for entry in st.session_state["history"]:
        #     st.markdown(f"You: {entry['query']}")
        #     st.markdown(f"Assistant: {entry['response']}")
        #     st.markdown("------------") 
    
if __name__ == "__main__":
	main()          