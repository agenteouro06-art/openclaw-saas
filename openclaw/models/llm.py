import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_llm(prompt):
    if not API_KEY:
        print("❌ Falta OPENROUTER_API_KEY en .env")
        return "{}"

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "Devuelve SOLO JSON válido para n8n. No expliques nada."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        res = r.json()

        print("🧠 RESPUESTA IA:", res)

        return res["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ Error IA:", e)
        return "{}"
