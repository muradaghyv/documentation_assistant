import time
from ..retrieval.search_engine import SearchEngine
from ..utils.logging_utils import setup_logger

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

        if results:
            logger.info("\nTop results:")
            for i, result in enumerate(results, 1):
                logger.info(f"\nResult {i}:")
                logger.info(str(result))
        else:
            logger.info("There is no result!")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    
def main():
    """Running the test queries"""
    queries = [
        "How do I create a virtual environment in Python?",
        "What are Django models?",
        "How to handle exceptions in Python?"   
    ]

    for query in queries:
        test_search(query=query)

if __name__ == "__main__":
    main()
        
