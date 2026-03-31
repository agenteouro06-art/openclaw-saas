import time
import requests
import os
from agent.planner import plan
from agent.executor import execute
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

last_update_id = 0

def get_updates():
    global last_update_id

    try:
        response = requests.get(f"{URL}/getUpdates?offset={last_update_id + 1}")
        data = response.json()

        print("📡 RAW TELEGRAM:", data)  # 🔥 DEBUG CLAVE

        if not data.get("ok"):
            print("❌ ERROR TELEGRAM:", data)
            return []

        return data.get("result", [])

    except Exception as e:
        print("❌ ERROR REQUEST:", e)
        return []

def send_message(chat_id, text):
    try:
        requests.post(f"{URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })
    except Exception as e:
        print("❌ ERROR ENVIANDO:", e)

print("🔥 BOT ACTIVO (OPENCLAW)")

while True:
    updates = get_updates()

    for update in updates:
        last_update_id = update["update_id"]

        if "message" in update and "text" in update["message"]:
            chat_id = update["message"]["chat"]["id"]
            user_text = update["message"]["text"]

            print(f"📩 {chat_id}: {user_text}")

            try:
                task = plan(user_text)
                result = execute(task)

                send_message(chat_id, f"🚀 Resultado:\n{result}")

            except Exception as e:
                send_message(chat_id, f"❌ Error: {str(e)}")

    time.sleep(2)
