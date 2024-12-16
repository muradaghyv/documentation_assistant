from dataclasses import dataclass
from typing import List

@dataclass
class RetrievalConfig:
    """Defining configuration for the retrieval system."""

    # Number of documents to retrieve
    top_doc: int = 5

    # Threshold for similarity comparison
    threshold: float = 0.5

    # Maximum length of context (in characters)
    max_len_context : int = 1000

    # Model name used for embedding
    model_name = "all-MiniLM-L6-v2"

    chunk_overlap = 200