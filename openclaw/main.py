import requests
import time
import os
from dotenv import load_dotenv

# 🔥 Cargar .env correctamente
load_dotenv(dotenv_path=".env")

from agent.planner import plan
from agent.executor import send_to_n8n

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    print("❌ TELEGRAM_TOKEN NO CARGADO")
    exit()

URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
