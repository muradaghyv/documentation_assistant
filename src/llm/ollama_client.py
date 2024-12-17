import requests
from ..utils.logging_utils import setup_logger

logger = setup_logger(__name__)

class OllamaClient:
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_endpoint = f"{self.base_url}/api/generate"
    
    def generate_response(self, prompt: str, system_prompt: str = None, temperature: float = 0.5) -> str:
        """Generating response from Ollama."""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,    
                # Add parameters to control response
                "temperature": temperature,
                "top_p": 0.9,
                "max_tokens": 500
            }
            if system_prompt: 
                payload["system"] = system_prompt

            response = requests.post(self.api_endpoint, json=payload)
            response.raise_for_status()
            
            return response.json().get("response", "")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            raise


            
        