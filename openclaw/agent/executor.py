from models.llm import ask_llm

def execute(task):
    if task["action"] == "create_workflow":

        description = task["description"]

        prompt = f"""
Eres experto en n8n.

Crea un workflow COMPLETO y FUNCIONAL para:
{description}

REGLAS:
- Solo usa nodos reales:
  webhook, httpRequest, set, if, function, respondToWebhook, gmail, telegram
- No inventes nodos
- Devuelve SOLO JSON válido
"""

        return ask_llm(prompt)

    return "No se pudo ejecutar"
