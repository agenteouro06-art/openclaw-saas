from marketplace.scraper import search_workflows, get_workflow_json

def find_real_workflow(user_prompt):
    results = search_workflows(user_prompt)

    if not results:
        return None

    best = results[0]
    workflow_id = best.get("id")

    workflow_json = get_workflow_json(workflow_id)

    return workflow_json
