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