import requests
from typing import List
from ..retrieval.search_result import SearchResult
from ..llm.prompt_templates import PromptTemplates
from ..utils.logging_utils import setup_logger

logger = setup_logger(__name__)

class OllamaClient:
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_endpoint = f"{self.base_url}/api/generate"

    def generate_response(self, question: str, search_results: List[SearchResult],
                          system_prompt: str = PromptTemplates.SYSTEM_PROMPT,
                          temperature: float = 0.5, max_tokens: int = 1200) -> str:
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
        try:
            # Combining text from the retrieval system results
            context = "\n\n".join(
                f"Source: {result.metadata.get('source', 'unknown')}\n{result.document}"
                for result in search_results
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
                "search_results": search_results,
                "llm_response": final_response
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            raise
        


            
        