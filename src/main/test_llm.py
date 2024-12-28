import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import time
from src.utils.logging_utils import setup_logger
from src.retrieval.search_engine import SearchEngine
from src.llm.ollama_client import OllamaClient

logger = setup_logger(__name__)

def test_search_generate(query: str):
    """Searching relevant information and generating response according to this search."""
    logger.info(f"\nTesting query: {query}")

    try: 
        searcher = SearchEngine()
        llm_client = OllamaClient()

        # Main process
        starting_time = time.time()
        search_result = searcher.search(query=query) # Result of the retrieval system
        result = llm_client.generate_response(question=query, search_results=search_result) # Final result
        processing_time = time.time() - starting_time

        # Logging the results
        logger.info(f"\nResults generated in {processing_time} seconds.")
        logger.info(f"\nQuery: {query}")

        logger.info(f"\nLLM response: \n{result['llm_response']}")
        
    except Exception as e:
        logger.error(f"An error occured: {str(e)}")

def main():
    """Running the queries."""
    q = input(str)
    test_queries = [
        q
    ]

    for query in test_queries:
        test_search_generate(query=query)

if __name__ == "__main__":
    main()