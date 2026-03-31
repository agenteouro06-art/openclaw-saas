from agent.planner import plan
from agent.executor import execute

def main():
    print("🔥 OPENCLAW SAAS ACTIVADO")

    while True:
        user_input = input("\n🧠 ¿Qué flujo quieres crear?\n> ")

        if user_input.lower() in ["exit", "salir"]:
            break

        task = plan(user_input)
        result = execute(task)

        print("\n🚀 RESULTADO:\n")
        print(result)


if __name__ == "__main__":
    main()
