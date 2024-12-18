# Personal Documentation Assistant 
This project involves creating a personal documentation assistant chatbot for helping developers. The RAG (Retrieval-Augmented Generation) technology is used for extracting the necessary information from the documentations for more accurate and reliable answers. 

Initially, there are 2 documentations: Python & Django. RAG system will be applied to these 2 formats. After the initial demo version is built successfully, additional programming languages and frameworks will be added, such as C/C++, JavaScript, Node.js, FastAPI, and so on. 

## The First Part
* Project started with the downloading of Python and Django documentations. Python documentation has been downloaded from its official website as zipped folder. 
* Django documentation has been scraped through its official GitHub repository. 
* Downloader scripts for both Python and Django are available in this class as seperate methods: `src.data.downloader.DocumentationDownloader`.
* Downloaded documentations are saved in `data/raw/`. *python_docs/* consists of Python documentation, whereas *django_docs* consists of Django documentation.

## The second part
* The second part of the project involved text processing and chunking steps. 
* Python documentation is unzipped and all .html files through different folders are parsed and read. Then standard chunking process has been applied to the read Python documentation files.
* As because all Django documentation files were in .txt format, it was a little bit easy to read and parse them. After parsing, chunking has been applied to this documentation. 
* Processing and chunking have been done using **src/data/processor.py** script. 
* Each documentation has its unique format, so they need different processing and chunking tricks, therefore main processing files have been separated inside the `src/main/` folder. (*process_python* & *process_python* scripts).

## The third part
The third part is one of the most important parts. This step involved 2 main processes: **embedding generation** and **vector (embedding) storing**. 
* Processed and chunked documentation files are given to the *Sentence Transformer* model for embedding generation;
* Vector database for storing embeddings have been initialized parallelly;
* Generated embeddings are stored in Vector Database which was created with the help of ChromaDB.

## The forth part
The most important step: **Retrival**.
* Firstly, input query is processed:
    * cleaned, normalized;
    * embedded. 
* Then, with the help of search method inside the VectorStore class, the most similar documentations are searched within vector database according to the input query embedding. 
* After the most relevant information is found, this information is extracted and decoded to the normal format. 

## The fifth part
After retrieval mechanism has been constructed, the Large Language Model can be integrated with the retrieval system. With the help of LLM models, answers can be more interactive, coherent and more natural. 
* Ollama models are used for this integration: llama-2. For starting point, I used **llama-2** model, but I think *llama-3.1* model can be used for more accurate and better responses.
* LLM integration has been accomplished by these steps:
    * Firstly, Ollama Client has been defined with the help of `src.llm.ollama_client` script;
    * OllamaClient object uses *generate_response()* method for generating LLM response.              *generate_response()* method takes 2 main inputs: **input query** entered by an user and **search_result** which is the result of the retrieval system. In other words, **search_results** is the relevant information based on the input query extracted from the documentation. These 2 inputs are fed into the LLM model for generating response.
    * The result of retrieval mechanism is derived by **search** method of **SearchEngine** object.
* `src.main.test_llm` is for testing llm response.