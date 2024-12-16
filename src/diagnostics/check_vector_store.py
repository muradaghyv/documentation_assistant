import logging
from ..database.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_vector_store():
    """Check the contents of the vector store."""
    try:
        vector_store = VectorStore()
        
        # Get collection stats
        collection = vector_store.collection
        collection_stats = collection.count()
        
        logger.info(f"Number of documents in collection: {collection_stats}")
        
        # Get a sample of documents if any exist
        if collection_stats > 0:
            sample = collection.peek(limit=2)
            logger.info("\nSample documents:")
            for idx, (doc, metadata) in enumerate(zip(sample['documents'], sample['metadatas'])):
                logger.info(f"\nDocument {idx + 1}:")
                logger.info(f"Source: {metadata.get('source', 'unknown')}")
                logger.info(f"Content preview: {doc[:200]}...")
        else:
            logger.warning("No documents found in the vector store!")
            
    except Exception as e:
        logger.error(f"Error checking vector store: {str(e)}")
        raise

if __name__ == "__main__":
    check_vector_store()