# ollama_client.py
import requests
import os

OLLAMA_API = os.getenv("OLLAMA_API", "http://127.0.0.1:11434")

def generate(prompt: str, model: str = "llama3") -> str:
    url = f"{OLLAMA_API}/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a security assistant."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["message"]["content"]
    except Exception as e:
        return f"[Error contacting Ollama: {e}]"