from pathlib import Path
from typing import Generator
from ..schema.document import ProcessedDocument
from ..utils.file_utils import get_data_directory

class DocumentLoader:
    def __init__(self):
        self.processed_dir = get_data_directory() / "processed"
    
    def load_documents(self) -> Generator[ProcessedDocument, None, None]:
        """Loading all processed documents."""
        # Loading Python docs
        python_dir = self.processed_dir / "processed_python"
        for file_path in python_dir.glob("*.txt"):
            yield self._load_single_document(file_path, "python")
        
        # Loading Django docs
        django_dir = self.processed_dir / "processed_django"
        for file_path in django_dir.glob("*.txt"):
            yield self._load_single_document(file_path, "django")
        
    def _load_single_document(self, filepath: Path, source: str) -> ProcessedDocument:
        """Load a single document file."""
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        return ProcessedDocument.from_file(
            file_path=filepath,
            content=content,
            source=source
        )