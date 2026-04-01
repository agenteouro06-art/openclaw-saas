import requests
import time
import os
from dotenv import load_dotenv

# 🔥 CARGAR VARIABLES DE ENTORNO
load_dotenv(dotenv_path=".env")

from agent.planner import plan
from agent.executor import send_to_n8n

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# 🚨 VALIDACIÓN CRÍTICA
if not TELEGRAM_TOKEN:
    print("❌ ERROR: TELEGRAM_TOKEN no cargado desde .env")
    exit()

URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

print("🔑 TOKEN CARGADO:", TELEGRAM_TOKEN[:10], "...")

last_update_id = 0


# 📡 OBTENER MENSAJES
def get_updates():
    global last_update_id

    try:
        response = requests.get(f"{URL}/getUpdates?offset={last_update_id + 1}", timeout=10)
        data = response.json()

        if not data.get("ok"):
            print("❌ Error Telegram:", data)
            return []

        return data.get("result", [])

    except Exception as e:
        print("❌ Error conexión Telegram:", e)
        return []


# 📤 ENVIAR MENSAJE
def send_message(chat_id, text):
    try:
        requests.post(f"{URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        }, timeout=10)
    except Exception as e:
        print("❌ Error enviando mensaje:", e)


print("🔥 BOT ACTIVO (OPENCLAW MARKETPLACE MODE)")


# 🔁 LOOP PRINCIPAL
while True:
    updates = get_updates()

    for update in updates:
        try:
            last_update_id = update["update_id"]

            if "message" not in update:
                continue

            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            print(f"📩 {chat_id}: {text}")

            if not text:
                continue

            # 🧠 AVISO INICIAL
            send_message(chat_id, "🧠 Buscando workflow real del marketplace...")

            # 🔎 PLANIFICACIÓN (IA + MARKETPLACE)
            workflow = plan(text)

            if not workflow:
                send_message(chat_id, "❌ No se pudo generar workflow válido")
                continue

            print("✅ WORKFLOW GENERADO:", workflow)

            send_message(chat_id, "🚀 Enviando workflow a n8n...")

            # 🚀 CREAR EN N8N
            response = send_to_n8n(workflow)

            print("📦 RESPUESTA N8N:", response)

            send_message(chat_id, f"✅ Workflow creado correctamente:\n{response}")

        except Exception as e:
            print("❌ Error general:", e)
            send_message(chat_id, "❌ Error procesando solicitud")

    time.sleep(2)
