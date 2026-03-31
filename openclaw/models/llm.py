import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def chat(prompt):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",  # 🔥 CLAVE
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "OpenClaw SaaS"
            },
            json={
                "model": "anthropic/claude-3-haiku",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000
            },
            timeout=30
        )

        data = response.json()

        if "error" in data:
            print("❌ Error IA:", data)
            return "Error IA"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ Exception IA:", e)
        return "Error IA"
