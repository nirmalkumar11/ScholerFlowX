import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

payload = {
    "model": "qwen2.5-coder:3b",
    "prompt": "Reply with only: CONNECTION_SUCCESS",
    "stream": False
}

response = requests.post(OLLAMA_URL, json=payload)

print(response.json()["response"])