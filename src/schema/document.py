from dataclasses import dataclass
from typing import Optional

@dataclass
class ProcessedDocument:
    """Creates an object from processed .txt files."""
    id: str
    content: str
    metadata: dict
    embedding: Optional[list] = None

    @classmethod
    def from_file(cls, file_path: str, content: str, source: str):
        """Create a processed document from file content."""
        return cls(
            id=str(file_path),
            content=content,
            metadata={
                "source": source,
                "filepath": str(file_path)
            }
        )