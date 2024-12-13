from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
from ..config.embedding_config import EmbeddingConfig

class EmbeddingManager:
    def __init__(self, config: EmbeddingConfig = EmbeddingConfig()):
        self.config = config
        self.model = SentenceTransformer(self.config.model_name)

    def create_embedding(self, text: str) -> np.ndarray:
        """Embedding generation for a single text."""
        return self.model.encode(text, convert_to_numpy=True)
    
    def create_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Embeddings generation for multiple texts."""
        return self.model.encode(texts, convert_to_numpy=True)
    