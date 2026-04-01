def validate_workflow(wf):
    if not wf:
        return False
    
    required = ["nodes", "connections", "settings"]

    for r in required:
        if r not in wf:
            return False

    if not isinstance(wf["nodes"], list):
        return False

    return True
