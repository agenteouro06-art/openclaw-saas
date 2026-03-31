import yaml
from agent.planner import plan
from agent.executor import execute

def main():
    print("🧠 OPENCLAW SaaS iniciado")
    
    while True:
        user_input = input("\n👉 ¿Qué flujo quieres crear?:\n> ")
        
        if user_input.lower() in ["exit", "salir"]:
            print("👋 Cerrando...")
            break
        
        # 🧠 PLANIFICAR
        task = plan(user_input)
        
        # ⚙️ EJECUTAR
        result = execute(task)
        
        print("\n✅ RESULTADO:")
        print(result)

if name == "main":
    main()
