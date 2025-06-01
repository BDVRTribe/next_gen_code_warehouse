import os
import json
from datetime import datetime, timezone
from warehouse.logger import log_undo_action, log_event  # Import your logging tools

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

    filename_safe = name.lower().replace(" ", "_")
    filepath = os.path.join(directory, f"{filename_safe}.json")

    # Determine if it's a new snippet or an overwrite
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            snapshot_before = json.load(f)
        action_type = "edit"
    else:
        snapshot_before = None
        action_type = "add"

    # Log undo action
    log_undo_action(
        action_type=action_type,
        language=language.lower(),
        filename=f"{filename_safe}.json",
        snapshot_before=snapshot_before
    )

    # Save the new/updated snippet
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(snippet, f, indent=2)

    print(f"✅ Snippet '{name}' saved to {filepath}")
    
    # Log event
    log_event(action=action_type, name=name, language=language.lower())


def undo_last_action():
    """
    Undo the most recent snippet action (add, edit, or delete) based on the latest undo log.
    """
    import glob

    log_files = sorted(glob.glob("undo_logs/*.json"), reverse=True)
    if not log_files:
        print("❌ No undo logs found.")
        return

    last_log = log_files[0]
    with open(last_log, "r", encoding="utf-8") as f:
        data = json.load(f)

    path = os.path.join(SNIPPET_DIR, data["language"], data["filename"])

    action_type = data["action_type"]
    snapshot = data["snapshot_before"]

    if action_type == "add":
        if os.path.exists(path):
            os.remove(path)
            print(f"🗑 Removed snippet '{data['filename']}' (undo of add).")
        else:
            print("⚠️ Nothing to remove. File not found.")

    elif action_type == "edit":
        if snapshot:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(snapshot, f, indent=2)
            print(f"↩ Reverted changes to '{data['filename']}' (undo of edit).")
        else:
            print("⚠️ No snapshot available to restore.")

    elif action_type == "delete":
        if snapshot:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(snapshot, f, indent=2)
            print(f"♻ Restored deleted snippet '{data['filename']}' (undo of delete).")
        else:
            print("⚠️ No snapshot available to restore.")

    else:
        print("❌ Unknown undo action type.")

    # Clean up the undo log
    os.remove(last_log)
    print("🧹 Undo log entry removed.")

def restore_snapshot(action):
    """
    Restore a specific snapshot from the undo log entry (used by undo_browser).
    """
    language = action.get("language")
    filename = action.get("filename")
    snapshot = action.get("snapshot_before")

    if not all([language, filename, snapshot]):
        print("❌ Incomplete undo entry. Cannot restore.")
        return

    path = os.path.join(SNIPPET_DIR, language, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)
        print(f"✅ Restored '{filename}' in '{language}' from snapshot.")
    except Exception as e:
        print(f"⚠️ Failed to restore file: {e}")


