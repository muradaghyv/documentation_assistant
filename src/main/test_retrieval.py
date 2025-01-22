import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import time
from src.retrieval.search_engine import SearchEngine
from src.utils.logging_utils import setup_logger

logger = setup_logger(__name__)

def test_search(query: str) -> None:
    """Test the search engine with sample query."""
    try:
        searcher = SearchEngine()

        # Time the search
        start_time = time.time()
        results = searcher.search(query=query)
        processing_time = time.time() - start_time

        # Logging results
        logger.info(f"Found {len(results)} in {processing_time} seconds.")
        documents = []

        if results:
            documents = [str(document) for document in results]
        else:
            logger.info("There is no result!")
        
        if documents:
            reranked_results = searcher.ranking(query=query, documents=documents)
            for index, (doc, score) in enumerate(reranked_results):
                logger.info(f"\nResult {index}: ")
                logger.info(f"\nRanking Score: {score}")
                logger.info(f"\nDocument: {doc}")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    
def main():
    """Running the test queries"""
    q = input(str)
    queries = [
        q  
    ]

    for query in queries:
        test_search(query=query)

if __name__ == "__main__":
    main()
        
