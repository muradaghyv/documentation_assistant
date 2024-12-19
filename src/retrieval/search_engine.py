from typing import List, Dict, Any
from ..config.retrieval_config import RetrievalConfig
from ..database.vector_store import VectorStore
from .query_processor import QueryProcessor
from .search_result import SearchResult
from ..llm.ollama_client import OllamaClient
from ..utils.logging_utils import setup_logger

logger = setup_logger(__name__)

class SearchEngine:
    def __init__(self):
        self.vector_store = VectorStore()
        self.query_processor = QueryProcessor()
        self.llm_client = OllamaClient()
    
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
