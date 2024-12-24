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

## Notes 16.12.2024
* Retrieval configuration parameters are set;
* check_vector_store script added for checking whether vector database is in normal format or not. Path to the diagnostics file: `src/diagnostics/check_vector_store.py`;
*P.S. The result of this diagnostics is that: vector databse works normal.*
* The script for cleaning, normalizig and embedding the input query is added (`src/retrieval/querry_processor.py`);
* Vector store script is changed. Main functions:
    * search function is updated;
    * embedding of the input query is in array format which is not accepted by the transformer model. This embedding is changed to list format.
* Search Engine class is defined. The main method, **search()** searchs for the relevant information on the documents and extracts the relevant information in the form of **SearchResult** class form;
* logging function is added to the utilities for pre-defined and consisted formatting.

### TODO
* Investigating different types of chunking methods (P.S. Look at the LinkedIn post about RAG system);
* Deeply investigate and learn the retrieval phase coding. Understand each detail of these codes. 
* After understanding each part of the code, I can pass to the next stage: Local LLM integration. This will be fun. 

## Notes 17.12.2024
* LLM integration is unsuccessful. I cannot run *test_llm.py* script. The error is because of the **response** parameter. When I initialize ollama client, I am doing something wrong that creates a problem, and I cannot run the code. 
* Despite it is not running currently, I have written the base for LLM integration. I think the structure is okay and if I solve that problem, the integration will be completely successful.
* Inside the **response_generator** script, `generate_response` method is created. The interesting point is that this method uses `generate_response` method of **ollama_client** script. `OllamaClient.generate_response` method uses the methods of *requests* library. If I am creating response like that, why didn't I use *requests* library and its methods inside the **response_generator** script directly? **_I have to look at it._**
* As I said, LLM integration didn't work out, but it doesn't mean I am giving up on it. 

### Updates
* I have fixed problems. Now, it is working quite normal. There qere 2 problems: inside the `src/llm/prompt_templates_py` script, I forgot to return the result of **cls** method. Therefore empty prompt was directed to the Ollama model. I have fixed it. The other problem was inside the `src/llm/ollama_client.py` script. When I looked through different documentation inside Ollama's official repo, I have found another type of code for generating response: 
    ```python
    response = requests.post("http://localhost:11434/api/generate", json=payload, stream=False)
    json_data = json.loads(response.text)
    return (json.dumps(json.loads(json_data["response"]), indent=2))
    ```
    * This was giving error, although I have fixed empty prompt problem, I have adjusted to that form:
    ```python
    response = requests.post(self.api_endpoint, json=payload)
    response.raise_for_status()

    return response.json().get("response", "")
    ```

### TODO
* Although I have succeeded to integrate the retrieval system with local LLM integration, there are some points that I did not understand quite well. I have to look thorugh them again and again. I have to understand every bit of the codes.
* Creating interface for this project would be great. I have to check it out.
* Installation and usage (especially *ollama serve* and other ollama terminal operations) remained unclear for me. I have to check them all. 

## Notes 18.12.2024
* Modifying **OllamaClient** class so that generating response is done inside the client directly. So, there is no need to use **ResponseGenerator** class;
* Deleted **ResponseGenerator** class and script;
* Adding comments and documentations to **OllamaClient** class for better explainability;

* I have looked through the codes and explained overall. However, there are some points that remained unclear to me, especially:
    * `src/retrieval/search_result.py`,
    * `src/retrieval/search_engine.py`.
* Actually, I have understood almost everything, but some tiny details are needed for further clarification.

* After this, I can start for constructing interface for this RAG project.

### TODO
* `src.retrieval.search_engine` script may be modified. Eliminate *retrieval_generate* method. Because inside the `src.main.test_llm` script, **OllamaClient** can be used generating response, and **search** method of *SearchEngine* object can be defined for extracting the relevant information from the documentation. Codes need to be more compact. Therefore, analyze it carefully.

## Notes 19.12.2024
* **OllamaClient** class modified. *generate_response()* method modified so that it generates an LLM response and returns all other results directly. 
* So, inside the `src.main.test_llm` script `src.llm.ollama_client` script is used for generating and showing responses, not `src.retrieval.search_engine` script.
* Modifying **OllamaClient** class gives us opportunity for more flexibility and simple structured codes. Therefore, I tried to cancel out abstractions of different functions over themselves for more simplicity.
* As because I am working on another project, I couldn't run the code, so I do not know, whether it will run or not. So, the first thing is to check out whether this version will work or not. 

* After ensuring LLM integration with retrieval system works fine, I can pass to the next stage which is building interface for this program. I have to decide which tool I will use for integration: streamlit, RestAPI, FastAPI, Flask or something else. One of main points is to determine which tool I can use for this objective.
* Another important point is that, which data should I add to the back-end for making this system work properly? I mean integrating the current system with the interactive interface will be challenging.

## Notes 23.12.2024
* Interface is built for easy usage;
* Interface is built with streamlit;
* added project root to the Python root. 

I have to note that for the initial version model gives a response according to the input, but I have to upgrade it so that: it has history and it can take sequential queries.

## Updates 24.12.2024
* Although the interface was giving unexplainable results yesterday, it works normal today. The final step was building an interface for the project and it has been done. From now, the further adjustments and improvements are needed to be done.

### TODO:
* Interface works normal, but it needs to be improved:
    * Query input box can be freezed so that when scrolling the page, box remains on the same place. So, we can see query box in each time.
    * When inputting multiple queries sequentially, the page doesn't give me the response that I want. What I want is that when I input the query it should give the response under the previous response. It does this operation now, but it also gives warning about empty query. I do not know what happens, but it is not exactly as I want.
    * Adding history to the interface would be great, in this case user can see its previous chats or its previous queries. 
    * Storing history so that whenever program is run via `streamlit run src/interface/app.py` command, it shows me the previous chats.
    * Adding *New Chat* option in which an empty chat is created whenever *New Chat* button is pressed.

The first 3 bullet points about interface should be fixed, they are important. However, the rest part can be done later.

* LLM response can be improved so that:
    * Its response can be more complicated and longer.

* Retrieval system can be improved:
    * The search mechanism can be improved. As far as I know chromaDB collection object uses **cosine similarity** for finding a relevant information. I have to investigate that searching mechanism in a very detailed manner, then I might change some strategy. Also, other searching mechanisms should be investigated.

* Documentation should be improved:
    * Updating **README** file: I think it should be changed completely, overall information about project and brief description about each step is enough. More focus should be given to the installation and usage of the program. 
    * Adding documentation and comments to the all source codes. In this way, functions will be easier to understand and handle.

Project has been done successfully overall. However, it can be modified so that it is ready and practical for an end-user. For this purpose, the further improvements should go in this direction:
    *interface* => *retrieval* => *LLM Response* => *Documentation*.

### Latest Update
* I have tried to install and run the model from the scratch on my notebook and it worked quite well. 
* I only added streamlit library to the `requirements.txt` file. The rest part is enough for running the app. It works quite well.