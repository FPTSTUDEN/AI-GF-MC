import requests
from llm.prompts import SYSTEM_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:7b-instruct"

def generate_response(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "system": SYSTEM_PROMPT,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.5,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "num_predict": 80
        }
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=30)
    r.raise_for_status()

    return r.json()["response"].strip()
