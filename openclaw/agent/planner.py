import json
import re
from models.llm import ask_llm


def limpiar_json(texto):
    try:
        # 🔥 eliminar ```json y ```
        texto = re.sub(r"```json", "", texto)
        texto = re.sub(r"```", "", texto)

        # 🔥 quitar espacios basura
        texto = texto.strip()

        return json.loads(texto)

    except Exception as e:
        print("❌ Error limpiando JSON:", e)
        return None


def plan(user_input):
    print("🔎 Buscando workflow real...")

    prompt = f"""
Crea un workflow de n8n REAL y válido.

REGLAS:
- SOLO usar nodos:
  webhook, httpRequest, set, if, function, respondToWebhook, gmail, telegram
- NO inventar nodos como whatsapp
- JSON válido sin texto extra
- Debe incluir: nodes, connections, settings

OBJETIVO:
{user_input}
"""

    respuesta = ask_llm(prompt)

    if not respuesta:
        print("❌ IA no respondió")
        return None

    print("🧠 RESPUESTA LIMPIA:", respuesta)

    workflow = limpiar_json(respuesta)

    if not workflow:
        print("❌ Workflow inválido")
        return None

    # 🔥 VALIDACIÓN CLAVE
    if "nodes" not in workflow or "connections" not in workflow:
        print("❌ JSON no tiene estructura válida")
        return None

    print("✅ Workflow listo")
    return workflow
