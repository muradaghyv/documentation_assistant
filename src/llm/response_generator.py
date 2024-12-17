from typing import List
from .ollama_client import OllamaClient
from .prompt_templates import PromptTemplates
from ..retrieval.search_result import SearchResult
from ..utils.logging_utils import setup_logger

logger = setup_logger(__name__)

class ResponseGenerator:
    def __init__(self, model_name="llama2"):
        self.llm_client = OllamaClient(model_name=model_name)
    
    def generate_response(self, question: str, search_results: List[SearchResult]) -> str:
        """Generate a response based on the question and search result obtained by retrieval system."""
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
            response = self.llm_client.generate_response(prompt=prompt,
                                                         system_prompt=PromptTemplates.SYSTEM_PROMPT)
            
            return response
        
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
