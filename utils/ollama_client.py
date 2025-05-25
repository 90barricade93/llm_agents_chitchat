import json
import requests
import os
from typing import List, Dict, Optional

class OllamaClient:
    """
    Client voor communicatie met de Ollama LLM API.
    
    Gebruik:
    ```python
    llm = OllamaClient(model="openchat:latest")
    response = llm.generate_response("Hoe gaat het?")
    ```
    """
    
    def __init__(self, model: str = "openchat:latest", base_url: str = None, api_key: str = None):
        """
        Initialiseer de Ollama client.
        
        Args:
            model: Naam van het te gebruiken LLM model (bijv. "openchat:latest")
            base_url: Basis URL van de Ollama API (optioneel, haalt uit env OLLAMA_BASE_URL of gebruikt default)
            api_key: API key voor authenticatie (optioneel, haalt uit env OLLAMA_API_KEY)
        """
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY")
        self.model = model
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
    
    def generate_response(
        self, 
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """
        Genereer een antwoord op basis van het gespreksverloop.
        
        Args:
            messages: Lijst van berichten in het formaat [{"role": "user", "content": "..."}, ...]
            temperature: Creativiteit (0.0-1.0, hoger = creatiever)
            max_tokens: Maximale lengte van het antwoord in tokens
            **kwargs: Extra parameters voor de API-aanroep
            
        Returns:
            Het gegenereerde antwoord als string
        """
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                **kwargs
            }
        }
        
        try:
            response = self.session.post(
                url, 
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            response.raise_for_status()
            
            # Verwerk streaming response indien nodig
            if "stream" in kwargs.get("stream", False):
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode("utf-8"))
                        if "message" in chunk and "content" in chunk["message"]:
                            full_response += chunk["message"]["content"]
                return full_response
            else:
                return response.json().get("message", {}).get("content", "[GEEN ANTWOORD]")
                
        except requests.exceptions.RequestException as e:
            print(f"Fout bij het ophalen van LLM antwoord: {e}")
            return f"[FOUT: {str(e)}]"
    
    def __call__(self, *args, **kwargs):
        """Maak directe aanroep mogelijk: llm("Hoe gaat het?") -> str"""
        if isinstance(args[0], str):
            return self.generate_response([{"role": "user", "content": args[0]}])
        return self.generate_response(*args, **kwargs)

# Voorbeeldgebruik
if __name__ == "__main__":
    llm = OllamaClient(model="llama3")
    
    # Eenvoudige vraag-antwoord
    response = llm("Wat is de hoofdstad van Frankrijk?")
    print(f"Antwoord: {response}")
    
    # Conversatie met context
    conversation = [
        {"role": "user", "content": "Hoe heet jij?"},
        {"role": "assistant", "content": "Ik ben een AI assistent."},
        {"role": "user", "content": "Wat was mijn vorige vraag?"}
    ]
    response = llm(conversation)
    print(f"Conversatie: {response}")