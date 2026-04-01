import requests
import os

N8N_URL = os.getenv("N8N_URL")

def send_to_n8n(workflow):

    try:
        response = requests.post(
            N8N_URL,
            json=workflow,
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )

        print("📡 STATUS N8N:", response.status_code)
        print("📡 RESPUESTA N8N:", response.text)

        if response.status_code in [200, 201]:
            return "✅ Workflow creado correctamente"

        return f"❌ Error n8n: {response.text}"

    except Exception as e:
        return f"❌ Error conexión n8n: {str(e)}"
