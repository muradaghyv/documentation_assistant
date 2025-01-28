import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.llm.ollama_client import OllamaClient
from src.retrieval.search_engine import SearchEngine

from src.utils.interface_utils import display_history

def initialize_session_state():
    """Initiliazing session state."""
    if "llm_client" not in st.session_state:
        st.session_state["llm_client"] = OllamaClient(model_name="llama3.1:latest")
        st.session_state["search_engine"] = SearchEngine()
    if "history" not in st.session_state:
        st.session_state["history"] = []

def main():
    st.title("Documentation Search Assistant")
    st.write("""Ask questions about Python or Django.""")

    # Initiliazing the components
    initialize_session_state()
    llm_client = st.session_state["llm_client"]
    search_engine = st.session_state["search_engine"]
    
    query = st.chat_input("Input query: ", key="query")

    if query:
        try:
            with st.spinner("Generating response: "):
                search_results = search_engine.search(query)
                documents = [str(document) for document in search_results]
                _, reranked_documents = search_engine.ranking(query, documents)
                response = llm_client.generate_response(query, search_results, reranked_documents)
            
            st.session_state.history.append({
                "query": query,
                "response": response["llm_response"]
            })
            
            query = ""
        
        except Exception as e:
            st.warning("An error occurred while processing your request!")
    
    else:
        st.warning("Please enter your request!")    

# Displaying the query and relevant response
    display_history()
    
if __name__ == "__main__":
	main()          