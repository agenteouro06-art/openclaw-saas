import json
import re
from models.llm import ask_llm


# 🧠 PROMPT FUERTE (NO INVENTAR BASURA)
SYSTEM_PROMPT = """
Eres un experto en n8n.

REGLAS OBLIGATORIAS:
- Devuelve SOLO JSON válido
- NO expliques nada
- NO uses ```json
- NO inventes nodos inexistentes
- Usa SOLO nodos reales tipo: n8n-nodes-base.*
- Siempre incluye: name, nodes, connections
- NO incluyas "settings"
- JSON debe ser compatible con API n8n

Objetivo:
Adaptar o generar workflows reales de n8n según el request del usuario.
"""


# 🧠 EXTRAER JSON LIMPIO
def extract_json(text):
    try:
        # quitar ```json
        text = re.sub(r"```json|```", "", text).strip()

        # encontrar JSON dentro del texto
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None

        json_str = match.group(0)

        return json.loads(json_str)

    except Exception as e:
        print("❌ Error parseando JSON:", e)
        return None


# 🧹 LIMPIEZA PRO PARA N8N
def clean_workflow(workflow):

    # ❌ eliminar settings (causa error 400)
    if "settings" in workflow:
        del workflow["settings"]

    # ✅ asegurar estructura mínima
    if "nodes" not in workflow:
        return None

    if "connections" not in workflow:
        workflow["connections"] = {}

    # 🔧 limpiar nodos
    for node in workflow.get("nodes", []):

        # id obligatorio
        if "id" not in node:
            node["id"] = str(abs(hash(node.get("name", "node"))))

        # typeVersion obligatorio
        if "typeVersion" not in node:
            node["typeVersion"] = 1

        # asegurar parameters
        if "parameters" not in node:
            node["parameters"] = {}

    return workflow


# 🚀 PLAN PRINCIPAL
def plan(user_input):

    try:
        print("🔎 Buscando workflow real...")
        
        prompt = f"""
{SYSTEM_PROMPT}

Usuario pidió:
{user_input}

Devuelve el workflow listo para importar en n8n.
"""

        response = ask_llm(prompt)

        print("🧠 RESPUESTA IA:", response)

        # 🔥 soporta múltiples formatos de respuesta
        if isinstance(response, dict):
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            content = str(response)

        # 🧠 extraer JSON
        workflow = extract_json(content)

        if not workflow:
            print("❌ No se pudo extraer JSON")
            return None

        # 🧹 limpiar para n8n
        workflow = clean_workflow(workflow)

        print("✅ Workflow limpio:", workflow)

        return workflow

    except Exception as e:
        print("❌ Error en plan:", e)
        return None
