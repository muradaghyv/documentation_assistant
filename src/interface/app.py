import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st
from src.llm.ollama_client import OllamaClient
from src.retrieval.search_engine import SearchEngine

from src.utils.logging_utils import setup_logger

logger = setup_logger(__name__)

def initialize_session_state():
    """Initiliazing session state."""
    if "llm_client" not in st.session_state:
        st.session_state["llm_client"] = OllamaClient(model_name="llama3.1")
        st.session_state["search_engine"] = SearchEngine()

def main():
    st.title("Documentation Search Assistant")
    st.write("""Ask questions about Python or Django.""")

    # Initiliazing the components
    initialize_session_state()
    
    llm_client = st.session_state["llm_client"]
    search_engine = st.session_state["search_engine"]

    # Input query
    query = st.text_input("Input query: ")

    if st.button("Search"):
        if query:
            try:
                with st.spinner("Generating response: "):
                    search_results = search_engine.search(query)
                    response = llm_client.generate_response(query, search_results)
                
                st.markdown("### Answer: ")
                st.markdown(response["llm_response"])
            
            except Exception as e:
                logger.error(f"Error occurred when generating a response: {str(e)}")
                st.error("An error occurred while processing your request!")
        
        else:
            st.error("Please enter your request!")
    
if __name__ == "__main__":
    main()