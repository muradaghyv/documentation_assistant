from ..data.downloader import DocumentationDownloader
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    """Main function to download all documentation."""
    downloader = DocumentationDownloader()
    try:
        downloader.download_django_docs()
        logging.info("Downloading Django documentation!")
    except Exception as e:
        logging.error(f"Error loading Django documentation: {str(e)}")

if __name__ == "__main__":
    main()