def normalize_workflow(workflow: dict) -> dict:
    """
    Corrige automáticamente el workflow para que sea compatible con n8n
    """

    # ✅ Asegurar settings vacío (OBLIGATORIO)
    workflow["settings"] = {}

    # ✅ Asegurar nombre
    if "name" not in workflow:
        workflow["name"] = "Generated Workflow"

    # ✅ Corregir nodos
    for node in workflow.get("nodes", []):
        
        # Fix tipo nodo
        if not node["type"].startswith("n8n-nodes-base"):
            node["type"] = f"n8n-nodes-base.{node['type']}"

        # Asegurar typeVersion
        node["typeVersion"] = node.get("typeVersion", 1)

        # Asegurar position
        node["position"] = node.get("position", [0, 0])

        # Asegurar parameters
        node["parameters"] = node.get("parameters", {})

    return workflow
