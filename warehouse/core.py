import os
import json
from datetime import datetime, timezone
from warehouse.logger import log_undo_action, log_event  # Import your logging tools

SNIPPET_DIR = "snippets"

def store_snippet(language, code, description, tags=None, title=None):
    import os, json, uuid
    from datetime import datetime

    if tags is None:
        tags = []

    if title is None:
        title = f"snippet_{uuid.uuid4().hex[:8]}"

    snippet = {
        "title": title,
        "code": code,
        "description": description,
        "tags": tags,
        "created_at": datetime.utcnow().isoformat()
    }

    # Ensure the directory exists
    os.makedirs(f"snippets/{language}", exist_ok=True)

    # Save the file as: snippets/python/title.json
    path = f"snippets/{language}/{title}.json"
    with open(path, "w") as f:
        json.dump(snippet, f, indent=2)

    print(f"💾 Snippet stored at {path}")


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


