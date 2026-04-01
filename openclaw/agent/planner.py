from models.llm import ask_llm
from models.parser import extract_json
from agent.normalizer import normalize_workflow

def plan(user_prompt: str):

    prompt = f"""
Eres un experto en n8n.

REGLAS OBLIGATORIAS:
- SOLO devuelve JSON válido
- Sin ```json
- Usa tipos reales: n8n-nodes-base.*
- Incluye SIEMPRE:
  - name
  - nodes
  - connections
  - settings: {{}}

Tarea:
{user_prompt}
"""

    response = ask_llm(prompt)

    print("🧠 RESPUESTA IA:", response)

    content = response["choices"][0]["message"]["content"]

    workflow = extract_json(content)

    if not workflow:
        return None

    # 🔥 NORMALIZAR
    workflow = normalize_workflow(workflow)

    print("✅ WORKFLOW LIMPIO:", workflow)

    return workflow
