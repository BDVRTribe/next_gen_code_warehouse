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

