# app/services/ollama_wrapper.py

import requests

class OllamaLLM:
    def __init__(self, model_name="gemma-3-4b-qat:latest"):
        self.model = model_name
        self.base_url = "http://localhost:11434/api/generate"

    def generate_answer(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
