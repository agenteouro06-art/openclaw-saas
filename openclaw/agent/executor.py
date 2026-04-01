import requests
import os

N8N_URL = os.getenv("N8N_URL")
N8N_API_KEY = os.getenv("N8N_API_KEY")

def send_to_n8n(workflow):
    url = f"{N8N_URL}/rest/workflows"

    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }

    r = requests.post(url, headers=headers, json=workflow)

    return r.text
