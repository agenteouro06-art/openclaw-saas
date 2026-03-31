from models.llm import chat
import json

SYS_N8N = """
Eres experto en n8n.

REGLAS CRÍTICAS:

- SOLO puedes usar estos nodos:
  - n8n-nodes-base.webhook
  - n8n-nodes-base.httpRequest
  - n8n-nodes-base.set
  - n8n-nodes-base.if
  - n8n-nodes-base.function
  - n8n-nodes-base.respondToWebhook
  - n8n-nodes-base.gmail
  - n8n-nodes-base.telegram

- PROHIBIDO inventar nodos
- PROHIBIDO usar nodos falsos

- SIEMPRE devuelve JSON válido
- SIN markdown
- SIN texto extra
- SOLO el JSON

Formato obligatorio:

{
 "name": "flujo",
 "nodes": [],
 "connections": {},
 "settings": {}
}
"""

def execute(task):
    prompt = f"{SYS_N8N}\n\nCrea este flujo:\n{task}"

    response = chat(prompt)

    print("🧠 RESPUESTA IA:", response)

    if not response:
        return fallback()

    try:
        if "```" in response:
            response = response.split("```")[1]

        wf = json.loads(response)

        if not isinstance(wf, dict):
            return fallback()

        wf["settings"] = {}

        return wf

    except Exception as e:
        print("⚠️ ERROR PARSE:", e)
        return fallback()


def fallback():
    return {
        "name": "Fallback seguro",
        "nodes": [
            {
                "id": "1",
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [200, 300],
                "parameters": {
                    "path": "fallback",
                    "httpMethod": "POST",
                    "responseMode": "lastNode"
                }
            }
        ],
        "connections": {},
        "settings": {}
    }
