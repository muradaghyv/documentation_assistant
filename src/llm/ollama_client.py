import requests
from typing import List
from ..retrieval.search_result import SearchResult
from ..llm.prompt_templates import PromptTemplates
from ..utils.logging_utils import setup_logger

logger = setup_logger(__name__)

class OllamaClient:
    def __init__(self, model_name: str = "llama3.1:latest", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_endpoint = f"{self.base_url}/api/generate"
    
    def check_server_status(self) -> bool:
        """Check if Ollama server is running and model is available"""
        try:
            # Check server
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code != 200:
                logger.error("Ollama server is not responding correctly")
                return False
            
            # Check if model exists
            models = [model["name"] for model in response.json().get("models", [])]
            if self.model_name not in models:
                logger.error(f"Model {self.model_name} not found. Available models: {models}")
                return False
                
            return True
            
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama server")
            return False

    def generate_response(self, question: str, search_results: List[SearchResult],
                          reranked_documents,
                          system_prompt: str = PromptTemplates.SYSTEM_PROMPT,
                          temperature: float = 0.65, max_tokens: int = 10000) -> str:
        """
        Generating a response with the help of Ollama Client. This response is generated according to 2 information:
        input query and relevant documentation extracted by RAG mechanism. They are joined ang fed into the LLM client.

        Args:
            question: input query given by an user.
            search_results: relevant information to the input query extracted via retrieval system.
            system_prompt: Default prompt given to the LLM client 
            temperature: controlling the randomness of the response. Lower value makes output less random
                and more deterministic. Greater value makes the output more random, but more creative.
            max_tokens: maximum token size of the response.
        Returns:
            LLM generated response.
        """
        if not self.check_server_status():
            raise ConnectionError("Ollama server not available or model not found")
        
        try:
            # Combining text from the retrieval system results
            context = "\n\n".join(
                f"Source: {result.metadata.get('source', 'unknown')}\n{documents}"
                for result, documents in zip(search_results, reranked_documents)
            )
            
            # Creating a prompt using template
            prompt = PromptTemplates.create_prompt(context=context, 
                                                   question=question)
            
            # Generate a response using LLM
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,    
                # Add parameters to control response
                "temperature": temperature,
                "top_p": 0.9,
                "max_tokens": max_tokens,
                "system": system_prompt
            }

            response = requests.post(self.api_endpoint, json=payload)
            response.raise_for_status() # Status code (2xx is successfull). 4xx for client errors & 5xx for server errors

            final_response = response.json().get("response", "")
            
            return {
                "query": question,
                "search_results": context,
                "llm_response": final_response
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            raise
        


            
        