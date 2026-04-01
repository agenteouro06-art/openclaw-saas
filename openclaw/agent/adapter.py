from models.llm import ask_llm
import json

def adapt_workflow(workflow, user_prompt):
    system_prompt = f"""
Eres experto en n8n.

Tienes este workflow REAL:

{json.dumps(workflow, indent=2)}

Tarea:
Modificar este workflow para cumplir:

{user_prompt}

Reglas:
- NO inventes nodos
- SOLO usa nodos existentes en el workflow
- Ajusta parámetros
- Mantén estructura válida

Devuelve SOLO JSON válido de n8n completo:
(name, nodes, connections, settings)
"""

    response = ask_llm(system_prompt)

    try:
        return json.loads(response)
    except:
        return None
