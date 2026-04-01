import json
import re

def extract_json(text: str):
    """
    Extrae JSON incluso si viene con ```json
    """

    try:
        # Quitar markdown
        text = re.sub(r"```json|```", "", text).strip()

        # Encontrar primer JSON válido
        start = text.find("{")
        end = text.rfind("}") + 1

        clean_json = text[start:end]

        return json.loads(clean_json)

    except Exception as e:
        print("❌ Error parseando JSON:", e)
        return None
