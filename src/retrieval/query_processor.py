import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.config.retrieval_config import RetrievalConfig
from sentence_transformers import SentenceTransformer

class QueryProcessor:
    """Processing user queries for information retrieval."""

    def __init__(self):
        self.model = SentenceTransformer(RetrievalConfig.model_name)       

    def process_query(self, query: str) -> str:
        """
        Processing raw query text, so that:
        - Removing unnecessary whitespaces;
        - Handling special characters;
        - Adding any context extraction 
        """
        query = " ".join(query.split())

        return query

    def embed_query(self, query: str):
        """Generate embeddings for the query."""
        processed_query = self.process_query(query=query)
        embedded_query = self.model.encode(processed_query)

        return embedded_query
    