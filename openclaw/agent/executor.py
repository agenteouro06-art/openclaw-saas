from models.llm import ask_llm
import json

def execute(task):
    if task["action"] == "create_workflow":

        description = task["description"]

        prompt = f"""
Eres experto en n8n.

Crea un workflow REAL y FUNCIONAL para:
{description}

REGLAS:
- SOLO usar nodos:
  webhook, httpRequest, set, if, function, respondToWebhook, gmail, telegram
- NO inventar nodos
- JSON limpio
- Incluir:
  name, nodes, connections, active, settings

FORMATO:

{{
 "name": "Nombre del workflow",
 "nodes": [],
 "connections": {{}},
 "active": false,
 "settings": {{}}
}}
"""

        response = ask_llm(prompt)

        try:
            data = json.loads(response)
            print("✅ JSON válido generado")
            return data
        except:
            print("⚠️ IA falló → usando fallback PRO")

            return {
                "name": "Pedido Restaurante WhatsApp",
                "nodes": [
                    {
                        "parameters": {
                            "path": "pedido",
                            "httpMethod": "POST",
                            "responseMode": "lastNode"
                        },
                        "name": "Webhook",
                        "type": "n8n-nodes-base.webhook",
                        "typeVersion": 1,
                        "position": [200, 300]
                    },
                    {
                        "parameters": {
                            "values": {
                                "string": [
                                    {
                                        "name": "respuesta",
                                        "value": "Pedido recibido ✅"
                                    }
                                ]
                            }
                        },
                        "name": "Set",
                        "type": "n8n-nodes-base.set",
                        "typeVersion": 1,
                        "position": [400, 300]
                    },
                    {
                        "parameters": {},
                        "name": "Responder",
                        "type": "n8n-nodes-base.respondToWebhook",
                        "typeVersion": 1,
                        "position": [600, 300]
                    }
                ],
                "connections": {
                    "Webhook": {
                        "main": [
                            [
                                {
                                    "node": "Set",
                                    "type": "main",
                                    "index": 0
                                }
                            ]
                        ]
                    },
                    "Set": {
                        "main": [
                            [
                                {
                                    "node": "Responder",
                                    "type": "main",
                                    "index": 0
                                }
                            ]
                        ]
                    }
                },
                "active": False,
                "settings": {}
            }

    return {"error": "No se pudo ejecutar"}
