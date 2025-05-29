import json
import os

REQUIRED_FIELDS = ["name", "language", "tags", "description", "code", "created_by", "created_at"]

def validate_snippet_file(file_path):
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"

    try:
        with open(file_path, "r") as f:
            snippet = json.load(f)
    except json.JSONDecodeError:
        return False, "Invalid JSON format."

    missing = [field for field in REQUIRED_FIELDS if field not in snippet]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    if not isinstance(snippet["tags"], list):
        return False, "'tags' must be a list."

    return True, "✅ Snippet is valid."

if __name__ == "__main__":
    path = input("Enter the path to the snippet JSON file: ").strip()
    valid, message = validate_snippet_file(path)
    print(message)

