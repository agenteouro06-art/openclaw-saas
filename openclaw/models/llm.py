import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_llm(prompt):
    if not API_KEY:
        print("❌ Falta OPENROUTER_API_KEY")
        return None

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        # 🔥 MODELO NUEVO (FUNCIONA)
        "model": "openrouter/auto",
        "messages": [
            {
                "role": "system",
                "content": "Eres experto en n8n. Devuelve SOLO JSON válido. No expliques nada."
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

        # 🔥 VALIDACIÓN REAL
        if "choices" not in res:
            print("❌ IA no devolvió choices")
            return None

        return res["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ Error IA:", e)
        return None
