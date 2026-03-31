import requests
import time
import os
from dotenv import load_dotenv
from agent.planner import plan
from agent.executor import execute

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

URL = f"https://api.telegram.org/bot{TOKEN}/"

last_update_id = None

print("🤖 BOT TELEGRAM ACTIVO...")

def get_updates():
    global last_update_id

    params = {"timeout": 100}

    if last_update_id:
        params["offset"] = last_update_id + 1

    response = requests.get(URL + "getUpdates", params=params)
    return response.json()

def send_message(chat_id, text):
    requests.post(URL + "sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })

while True:
    data = get_updates()

    if "result" in data:
        for update in data["result"]:
            last_update_id = update["update_id"]

            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")

                print(f"📩 {chat_id}: {text}")

                if text:
                    try:
                        task = plan(text)
                        result = execute(task)

                        send_message(chat_id, f"🚀 Resultado:\n{result}")

                    except Exception as e:
                        send_message(chat_id, f"❌ Error:\n{str(e)}")

    time.sleep(2)
