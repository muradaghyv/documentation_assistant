import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from sentence_transformers import CrossEncoder
from typing import List
from src.config.retrieval_config import RetrievalConfig
from src.database.vector_store import VectorStore
from src.retrieval.query_processor import QueryProcessor
from src.retrieval.search_result import SearchResult
from src.llm.ollama_client import OllamaClient
from src.utils.logging_utils import setup_logger

import torch

logger = setup_logger(__name__)

class SearchEngine:
    def __init__(self):
        self.vector_store = VectorStore()
        self.query_processor = QueryProcessor()
        self.llm_client = OllamaClient()
        self.encoder_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    
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
    
    def ranking(self, query, documents):
        pairs = [(query, document) for document in documents]
        scores = self.encoder_model.predict(pairs, activation_fct=torch.nn.Sigmoid())
        reranked_results = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
        reranked_documents = [doc for doc, score in reranked_results]
        
        return reranked_results, reranked_documents[:10]
