import os
import requests
import json

def ask_groq(prompt: str) -> str:
    """Sends a prompt to Groq and returns the response."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Warning: GROQ_API_KEY not set. Returning fallback content.")
        return "No API Key provided. This is a fallback generation."
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert developer maintaining a personal knowledge base and devlog. Write in a concise, professional markdown format."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code != 200:
            print(f"Groq API Error Detail: {response.text}")
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Groq API Error: {e}")
        return f"Failed to generate content: {e}"
