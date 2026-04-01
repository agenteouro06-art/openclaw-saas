import requests
import time
import os
from agent.planner import plan
from agent.executor import send_to_n8n

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

last_update_id = 0

def get_updates():
    global last_update_id

    try:
        response = requests.get(f"{URL}/getUpdates?offset={last_update_id + 1}")
        data = response.json()

        if not data.get("ok"):
            print("❌ Error Telegram:", data)
            return []

        return data.get("result", [])
    
    except Exception as e:
        print("❌ Error conexión Telegram:", e)
        return []


def send_message(chat_id, text):
    try:
        requests.post(f"{URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })
    except Exception as e:
        print("❌ Error enviando mensaje:", e)


print("🔥 BOT ACTIVO (OPENCLAW MARKETPLACE MODE)")

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

            send_message(chat_id, "🧠 Buscando workflow real...")

            # 🔎 PLAN (buscar + adaptar workflow)
            workflow = plan(text)

            if not workflow:
                send_message(chat_id, "❌ No se pudo generar workflow válido")
                continue

            send_message(chat_id, "🚀 Creando workflow en n8n...")

            # 🚀 ENVIAR A N8N
            response = send_to_n8n(workflow)

            print("📦 RESPUESTA N8N:", response)

            send_message(chat_id, f"✅ Workflow creado:\n{response}")

        except Exception as e:
            print("❌ Error general:", e)
            send_message(chat_id, "❌ Error procesando solicitud")

    time.sleep(2)
