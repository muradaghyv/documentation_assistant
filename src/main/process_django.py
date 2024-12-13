from ..data.processor import DocumentProcessor
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    """Main function for processing all documentations."""
    # Defining processor
    processor = DocumentProcessor()

    # Collecting chunks
    all_chunks = []

    # Processing Python documentation
    try:
        logging.info("Processing Django documentation . . .")
        all_chunks.extend(list(processor.process_django_docs()))
        processor.save_processed_chunks(all_chunks)
        logging.info("Processing and chunking completed!")
    except Exception as e:
        logging.error(f"Error processing Django documentation: {str(e)}")
    
if __name__ == "__main__":
    main()
    