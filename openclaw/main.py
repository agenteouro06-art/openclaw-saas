import requests
import time
import json
import os
from dotenv import load_dotenv
from agent.planner import plan
from agent.executor import execute

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

last_update_id = 0


def get_updates():
    global last_update_id

    try:
        response = requests.get(f"{URL}/getUpdates?offset={last_update_id + 1}")
        data = response.json()

        print("📡 RAW TELEGRAM:", data)

        if not data.get("ok"):
            return []

        return data.get("result", [])

    except Exception as e:
        print("❌ Error get_updates:", e)
        return []


def send_message(chat_id, text):
    try:
        requests.post(f"{URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })
    except Exception as e:
        print("❌ Error send_message:", e)


print("🔥 BOT ACTIVO (OPENCLAW)")

while True:
    updates = get_updates()

    for update in updates:
        try:
            last_update_id = update["update_id"]

            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            print(f"📩 {chat_id}: {text}")

            # 🧠 PLAN
            task = plan(text)

            # ⚙️ EXECUTE
            result = execute(task)

            # 🔥 ANTI-CRASH
            if isinstance(result, dict):
                output = json.dumps(result, indent=2)
            else:
                output = str(result)

            send_message(chat_id, f"🚀 Resultado:\n{output[:3500]}")

        except Exception as e:
            print("❌ Error:", e)

    time.sleep(2)
