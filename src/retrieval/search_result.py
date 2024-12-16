from typing import Dict

class SearchResult:
    def __init__(self, document: str, metadata: Dict, score: float):
        self.document = document
        self.metadata = metadata
        self.score = score
    
    def __str__(self):
        return (
            f"Source: {self.metadata.get('source', 'unknown')}\n"
            f"Score: {self.score}\n"
            f"Content: {self.document}\n"
            f"{'-'*80}\n"
        )