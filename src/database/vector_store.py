import numpy as np
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from pathlib import Path
from ..config.embedding_config import DatabaseConfig
from ..schema.document import ProcessedDocument
from ..embeddings.embedding_manager import EmbeddingManager

class VectorStore:
    def __init__(self,
                 db_config: DatabaseConfig = DatabaseConfig(),
                 embedding_manager: Optional[EmbeddingManager] = None):
        self.config = db_config
        self.embedding_manager = embedding_manager or EmbeddingManager()

        # Initializing ChromaDB
        self.client = chromadb.PersistentClient(
            path=self.config.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.config.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: List[ProcessedDocument]) -> None:
        """Adding documents to the vector store."""
        if not documents:
            return
        
        # Preparing data for ChromaDB
        ids = [str(doc.id) for doc in documents]
        texts = [doc.content for doc in documents]
        metadata = [doc.metadata for doc in documents]

        # Create embeddings
        embeddings = self.embedding_manager.create_embeddings(texts=texts)
        embeddings_list = embeddings.tolist() if isinstance(embeddings, np.ndarray) else [
            emb.tolist() if isinstance(emb, np.ndarray) else emb for emb in embeddings
        ]

        # Adding it to collection
        self.collection.add(ids=ids,
                            embeddings=embeddings_list, 
                            documents=texts,
                            metadatas=metadata)
        
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Searching for similar documents."""
        query_embedding = self.embedding_manager.create_embedding(text=query)
        embedding_list = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else [
            emb.tolist() if isinstance(emb, np.ndarray) else emb for emb in query_embedding
        ]

        results = self.collection.query(
            query_embeddings=[embedding_list],
            n_results=n_results,
            include=["documents", "distances", "metadatas"]
        )

        return results
    