from agent.retriever import find_real_workflow
from agent.adapter import adapt_workflow
from agent.validator import validate_workflow

def plan(user_prompt):
    print("🔎 Buscando workflow real...")
    
    wf = find_real_workflow(user_prompt)

    if not wf:
        print("⚠️ No encontrado, fallback")
        return None

    print("🧠 Adaptando workflow...")
    
    adapted = adapt_workflow(wf, user_prompt)

    if validate_workflow(adapted):
        print("✅ Workflow válido")
        return adapted

    print("❌ Workflow inválido")
    return None
