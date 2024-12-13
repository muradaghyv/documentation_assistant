from dataclasses import dataclass

@dataclass
class EmbeddingConfig:
    model_name: str = "all-MiniLM-L6-v2"
    embedding_dimension: int =  384
    chunk_overlap: int = 50

@dataclass
class DatabaseConfig:
    persist_directory: str = "data/vector_store"
    collection_name: str = "documentation_store"
    