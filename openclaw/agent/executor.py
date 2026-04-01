import requests
import os

N8N_URL = os.getenv("N8N_URL")
N8N_API_KEY = os.getenv("N8N_API_KEY")


def send_to_n8n(workflow):
    if not N8N_URL:
        return "❌ N8N_URL no definida"

    url = f"{N8N_URL}/api/v1/workflows"

    headers = {
        "Content-Type": "application/json"
    }

    # 🔥 SI HAY API KEY → usarla
    if N8N_API_KEY:
        headers["X-N8N-API-KEY"] = N8N_API_KEY

    try:
        response = requests.post(url, json=workflow, headers=headers)

        print("📡 STATUS N8N:", response.status_code)
        print("📡 RESPUESTA N8N:", response.text)

        if response.status_code == 401:
            return "❌ Unauthorized → revisa API KEY de n8n"

        if response.status_code >= 400:
            return f"❌ Error n8n: {response.text}"

        return response.json()

    except Exception as e:
        return f"❌ Error conexión n8n: {e}"
