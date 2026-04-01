import requests

def search_workflows(query):
    url = f"https://api.n8n.io/api/workflows?search={query}"
    
    try:
        r = requests.get(url)
        data = r.json()
        return data.get("data", [])
    except:
        return []

def get_workflow_json(workflow_id):
    url = f"https://api.n8n.io/api/workflows/{workflow_id}"
    
    try:
        r = requests.get(url)
        return r.json()
    except:
        return None
