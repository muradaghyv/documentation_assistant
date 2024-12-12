import zipfile
import re
from pathlib import Path
from typing import List, Dict, Generator
from bs4 import BeautifulSoup
from dataclasses import dataclass
from ..utils.file_utils import get_data_directory, create_directory

@dataclass
class DocumentChunk:
    """Represents a chunk of a documentation"""
    source: str     # "python" or "django"
    title: str      # Document or section title
    content: str    # Actual content
    path: str       # Original file path

class DocumentProcessor:
    def __init__(self):
        self.raw_dir = get_data_directory() / "raw"
        self.processed_dir = get_data_directory() / "processed"
        create_directory(self.processed_dir)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        # Removing multiple lines
        text = re.sub(r"\n+", "\n", text)

        # Removing multiple spaces
        text = re.sub(r"\s+", " ", text)

        # Remove HTML comments 
        text = re.sub(r"<!--.?-->", "", text)

        return text
    
    def split_into_chunks(self, text: str, max_chunk_size: int = 1000) -> List[str]:
        """Creates chunks with size of max_chunk_size parameter from the document."""
        chunks = []
        sentences = re.split(r'(?<=[.!?])\s+', text) # Splitting sentences from the document
        current_chunk = []
        current_size = 0

        for sentence in sentences:
            sentence_size = len(sentence)
            if current_size+sentence_size > 1000 and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def process_python_docs(self) -> Generator[DocumentChunk, None, None]:
        """Processing zipped Python documentation. Creating chunks from them."""
        python_zip = self.raw_dir / "python_docs/python-3.10-docs.zip"

        with zipfile.ZipFile(python_zip, "r") as zip_ref:
            for file_info in zip_ref.filelist:
                if file_info.filename.endswith(".html"):
                    with zip_ref.open(file_info) as f:
                        content = f.read().decode("utf-8")
                        soup = BeautifulSoup(content, "html.parser")

                        # Removing navigation, sidebars from the HTML content
                        for div in soup.find_all(["nav", "sidebar", "footer"]):
                            div.decompose()

                        # Getting the main content
                        main_content = soup.find("div", class_="body") 
                        if main_content:
                            # Separating the main text and title
                            text = self.clean_text(main_content.get_text())
                            title = soup.title.string if soup.title else ""
                            title = title.replace("/", "_")

                            # Splitting into chunks
                            chunks = self.split_into_chunks(text=text)
                            for i, chunk in enumerate(chunks):
                                yield DocumentChunk(
                                    source="python",
                                    title=f"{title} - Part {i+1}",
                                    content=chunk,
                                    path=file_info.filename
                                )
        
    def process_django_docs(self) -> Generator[DocumentChunk, None, None]:
        """Processing .txt Django documentation. Creating chunks from these .txt files."""
        django_dir = self.raw_dir / "django_docs/" 

        for txt_file in django_dir.glob("*.txt"):
            with open(txt_file, "r", encoding="utf-8") as f:
                content = f.read()

                # Extracting title from the filename or the first line
                title = txt_file.stem.replace("_", " ").title()

                # Clean text and chunking
                clean_content = self.clean_text(content)
                chunks = self.split_into_chunks(clean_content)

                for i, chunk in enumerate(chunks):
                    yield DocumentChunk(
                        source="django",
                        title=f"{title} - Part {i+1}",
                        content=chunk,
                        path=str(txt_file.relative_to(django_dir))
                    )

    def save_processed_chunks(self, chunks: List[DocumentChunk]) -> None:
        """Save processed chunks into the processed directory."""
        for source in ["python", "django"]:
            source_dir = self.processed_dir / f"processed_{source}"
            create_directory(source_dir)

            # Saving chunks into the created source folders
            source_chunks = [c for c in chunks if c.source==source]
            for i, chunk in enumerate(source_chunks):
                filename = f"{chunk.title.lower().replace(' ', '_')}_{i}.txt"
                filepath = source_dir / filename

                try:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(f"Title: {chunk.title}\n")
                        f.write(f"Source: {chunk.source}\n")
                        f.write(f"Original Path: {chunk.path}\n")
                        f.write("-" * 80 + "\n")
                        f.write(chunk.content)
                except Exception as e:
                    print(f"Error saving chunk to {filepath}: {str(e)}.")

def main():
    """Main function for processing all documentations."""
    # Defining processor
    processor = DocumentProcessor()

    # Collecting chunks
    all_chunks = []

    # Processing Python documentation
    print("Processing Python documentation . . .")
    all_chunks.extend(list(processor.process_python_docs()))

    # Procesing Django Documentation
    print("Processing Django documentation . . .")
    all_chunks.extend(list(processor.process_django_docs()))

    # Saving processed chunks
    print("Saving processed chunks . . .")
    processor.save_processed_chunks(all_chunks)

    print("Procesing and saving completed!")

if __name__ == "__main__":
    main()