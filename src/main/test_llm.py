import time
from ..utils.logging_utils import setup_logger
from ..retrieval.search_engine import SearchEngine

logger = setup_logger(__name__)

def test_search_generate(query: str):
    """Searching relevant information and generating response according to this search."""
    logger.info(f"\nTesting query: {query}")

    try: 
        searcher = SearchEngine()

        # Main process
        starting_time = time.time()
        result = searcher.retrieval_generate(query=query)
        processing_time = time.time() - starting_time

        # Logging the results
        logger.info(f"\nResults generated in {processing_time} seconds.")
        logger.info(f"\nQuery: {query}")

        logger.info(f"\nLLM response: \n{result['llm_response']}")

        # logger.info("\nThese documents were used: \n")
        # for i, doc in enumerate(result["search_results"], 1):
        #     logger.info(f"\nDocument {i}")
        #     logger.info(f"\nSource: {doc.source}")
        #     logger.info(f"Document preview: {doc.context[:300]} . . .")
        
    except Exception as e:
        logger.error(f"An error occured: {str(e)}")

def main():
    """Running the queries."""
    test_queries = [
        "How can I create virtual environment in Python?"
    ]

    for query in test_queries:
        test_search_generate(query=query)

if __name__ == "__main__":
    main()