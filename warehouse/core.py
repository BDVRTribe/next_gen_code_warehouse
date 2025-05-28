import os
import json
from datetime import datetime

def store_snippet(name, code, language, tags=None, description="", created_by="unknown"):
    """
    Store a code snippet in a standardized JSON format.
    """
    snippet = {
        "name": name,
        "language": language,
        "tags": tags or [],
        "description": description,
        "code": code,
        "created_by": created_by,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    # Create directory if it doesn't exist
    dir_path = os.path.join("snippets", language.lower())
    os.makedirs(dir_path, exist_ok=True)

    # Save as JSON file using snake_case name
    file_name = name.lower().replace(" ", "_") + ".json"
    full_path = os.path.join(dir_path, file_name)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(snippet, f, indent=2)

    print(f"✅ Snippet saved to {full_path}")
import json
import os

def store_snippet(name, code, language, filename="snippets.json"):
    snippet = {
        "name": name,
        "code": code,
        "language": language
    }

    # Create the file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)

    # Load existing snippets
    with open(filename, "r") as f:
        snippets = json.load(f)

    # Add the new one
    snippets.append(snippet)

    # Write back to file
    with open(filename, "w") as f:
        json.dump(snippets, f, indent=2)

    return snippet
def store_snippet(name, code, language):
    return {
        "name": name,
        "code": code,
        "language": language
    }

