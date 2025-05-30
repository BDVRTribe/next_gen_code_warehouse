import os
import json
from datetime import datetime, timezone

SNIPPET_DIR = "snippets"

def store_snippet(name, code, language, tags=None, description="", created_by="anonymous"):
    """
    Store a code snippet in a structured JSON file inside a language-specific directory.
    
    Parameters:
        name (str): The name of the snippet.
        code (str): The actual code as a string.
        language (str): Programming language the snippet belongs to.
        tags (list, optional): List of tags related to the snippet.
        description (str, optional): Short description of what the snippet does.
        created_by (str, optional): Origin of the snippet creation (default is "anonymous").
    """
    snippet = {
        "name": name,
        "language": language,
        "tags": tags or [],
        "description": description,
        "code": code,
        "created_by": created_by,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    directory = os.path.join(SNIPPET_DIR, language.lower())
    os.makedirs(directory, exist_ok=True)

    filename = os.path.join(directory, f"{name.lower().replace(' ', '_')}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(snippet, f, indent=2)

    print(f"✅ Snippet '{name}' saved to {filename}")
