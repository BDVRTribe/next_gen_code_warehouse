import json
import ast
from datetime import datetime

REQUIRED_FIELDS = ["name", "language", "tags", "description", "code", "created_by", "created_at"]

def validate_snippet(snippet):
    # Check required fields
    missing = [field for field in REQUIRED_FIELDS if field not in snippet]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    # Check tag structure
    if not isinstance(snippet["tags"], list):
        return False, "'tags' must be a list."

    # Check date format
    try:
        datetime.fromisoformat(snippet["created_at"].replace("Z", "+00:00"))
    except ValueError:
        return False, "'created_at' is not in ISO 8601 format."

    # Try compiling the code for syntax validation (Python only for now)
    if snippet["language"] == "python":
        try:
            ast.parse(snippet["code"])
        except SyntaxError as e:
            return False, f"Python syntax error: {e}"

    return True, "✅ Snippet is valid."
