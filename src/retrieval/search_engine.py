from typing import List, Dict, Any
from ..config.retrieval_config import RetrievalConfig
from ..database.vector_store import VectorStore
from .query_processor import QueryProcessor
from .search_result import SearchResult
from ..utils.logging_utils import setup_logger

from sentence_transformers import SentenceTransformer
from ..llm.response_generator import ResponseGenerator

logger = setup_logger(__name__)

class SearchEngine:
    def __init__(self):
        self.vector_store = VectorStore()
        self.query_processor = QueryProcessor()
        self.response_generator = ResponseGenerator()
    
    def search(self, query: str, n_results: int=RetrievalConfig.top_doc, score: float=RetrievalConfig.threshold) -> List[SearchResult]:
        """Searching for a relevant document."""
        try:
            # Processing query
            processed_query = self.query_processor.process_query(query=query)

            # Searching operation
            results = self.vector_store.search(
                query=processed_query,
                n_results=n_results
            )

            if not results or not results["documents"]:
                logger.info("No documents were found!")
                return []
            
            # Processing results
            search_results = []
            for doc, metadata, distance in zip(results["documents"][0], 
                                               results["metadatas"][0],
                                               results["distances"][0]):
                similarity_score = 1 - distance
                if similarity_score >= score:
                    search_results.append(SearchResult(document=doc, metadata=metadata, score=score))
            
            return search_results
        
        except Exception as e:
            logger.error(f"Error happened during retrieval process: {str(e)}")
            raise

    def retrieval_generate(self, query: str, n_results: int = RetrievalConfig.top_doc) -> Dict[str, Any]:
        """Generating LLM response according to extracted information."""
        try:
            # Searching relevant information
            search_results = self.search(query=query)
            
            # LLM response
            llm_response = self.response_generator.generate_response(question=query, search_results=search_results)

            return {
                "query": query,
                "search_results": search_results,
                "llm_response": llm_response
            }
        
        except Exception as e:
            logger.error(f"Error in generating response: {str(e)}")
            raise


