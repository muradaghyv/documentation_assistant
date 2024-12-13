from ..data.document_loader import DocumentLoader
from ..database.vector_store import VectorStore
from ..utils.file_utils import create_directory
import logging

# Configuring logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
def main():
    """Main function to embed documents and store it in the vector space."""
    try:
        # Create vector space directory.
        create_directory("data/vector_store")

        # Initialize components
        loader = DocumentLoader()
        vector_store= VectorStore()

        # Loading and processing documents in batches
        batch_size = 100
        current_batch = []
        total_processed = 0

        logging.info("Starting document processing and embedding . . .")

        for doc in loader.load_documents():
            current_batch.append(doc)

            if len(current_batch) >= batch_size:
                try:
                    vector_store.add_documents(current_batch)
                    total_processed += len(current_batch)
                    logging.info(f"Processed {total_processed} documents . . .")
                    current_batch = []
                except Exception as e:
                    logging.error(f"Error processing batch: {str(e)}")
                    raise
        
        if current_batch:
            vector_store.add_documents(current_batch)
            total_processed += len(current_batch)
        
        logging.info(f"Document embedding and storage completed!\nTotal embedded documents: {total_processed}.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()