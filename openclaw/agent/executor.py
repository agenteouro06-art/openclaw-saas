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
- PROHIBIDO usar nodos falsos (ej: imageTool, whatsappBusinessApi)

- SIEMPRE devuelve JSON válido
- SIN markdown
- SIN explicaciones
- SOLO el JSON

- El workflow debe ser COMPLETO y FUNCIONAL

Estructura obligatoria:

{
 "name": "nombre",
 "nodes": [],
 "connections": {},
 "settings": {}
}
"""

def execute(task):
    prompt = f"{SYS_N8N}\n\nCrea este flujo:\n{task}"

    response = chat(prompt)

    if not response:
        return "❌ IA no respondió"

    try:
        # 🔥 limpiar basura tipo ```json
        if "```" in response:
            response = response.split("```")[1]

        wf = json.loads(response)

        # 🔥 asegurar settings
        wf["settings"] = {}

        return wf

    except Exception as e:
        print("⚠️ IA devolvió mal JSON:", response)
        return generar_fallback()

def generar_fallback():
    return {
        "name": "Fallback básico",
        "nodes": [
            {
                "id": "1",
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [200, 300],
                "parameters": {
                    "path": "test",
                    "httpMethod": "POST",
                    "responseMode": "lastNode"
                }
            }
        ],
        "connections": {},
        "settings": {}
    }
