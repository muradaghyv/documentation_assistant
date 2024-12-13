## Notes 11.12.2024
Initially Python and Django are selected for the demo version. Hoever, in later parts, the number of programming languages and frameworks can be increased. 
* Python documentation has been installed from their official website. This documentation is stored inside `data/raw/python_docs` as zip folder. 
* Django documentation has been scraped from their official GitHub repository. This documentation has been saved as many .txt files inside the `data/raw/django_docs` folder. 

The scraping and downloading functions are methods of DocumentationDownloader class which is inside the `src/data` directory.

## Notes 12.12.2024
* Python documentation is unzipped and all html files are parsed and read. Then, all documents are chunked and saved in `data/processed/processed_python/`
* Django documentation is read and all .txt files are chunked. These files are saved in `data/processed/processed_django/`
* I must note that all documents inside these documentations are cleaned and normalized, then they were given to chunking process. All processes have been automatized in **src/data/processor.py** script.

The next stage is generation of embedding and vector space. Most probably, this job will be done during next days.

## Notes 13.12.2024
* Embedding and Database (for storing vector embeddings) configuration files are created;
* Embedding methods inside **EmbeddingManager** class are constructed for generation of embeddings for single and multiple texts;
* .txt files are converted to **ProcessedDocument** objects using `src/schema/document.py` and `src/data/document_loader.py` scripts;
* **ChromaDB** database is initialized, then methods for creating embeddings of processed documents and collecting these embeddings into this *vector store* are built;
* Downloading and text processing scripts are updated:
    * Running `src/data/downloader.py` or `src/data/processor.py` was respectively downloading the documentations of both Python & Django and processing Python & Django documents automatically and **together**. However, an end-user do not have to download all packages and process all packages. An end-user can download and process only selected documents. This gives him/her more flexibility and control on downloading and processing.