import json
import os
from datetime import datetime, timezone

LOG_FILE = "logs/activity.log"
UNDO_LOG_DIR = "undo_logs"

def log_event(action, name, language=None, details=None):
    """
    Logs a general action (create, update, delete) to the activity log.
    """
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "name": name,
        "language": language,
        "details": details or {}
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def log_undo_action(action_type, language, filename, snapshot_before=None):
    """
    Logs an undo snapshot before a destructive operation (e.g., delete or overwrite),
    including full file content and path for GUI-based restoration.
    """
    os.makedirs(UNDO_LOG_DIR, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
    undo_log_path = os.path.join(UNDO_LOG_DIR, f"{action_type}_{timestamp}.json")

    if snapshot_before is None:
        snapshot_before = {}

    # Ensure path is available
    if "path" not in snapshot_before:
        snapshot_before["path"] = os.path.join("snippets", language, filename)

    # Ensure code is captured
    if "code" not in snapshot_before:
        try:
            with open(snapshot_before["path"], "r", encoding="utf-8") as f:
                snapshot_before["code"] = f.read()
        except Exception as e:
            print(f"⚠️ Could not read code from {snapshot_before['path']}: {e}")
            snapshot_before["code"] = ""

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action_type": action_type,
        "language": language,
        "filename": filename,
        **snapshot_before  # Flatten snapshot data
    }

    with open(undo_log_path, "w", encoding="utf-8") as f:
        json.dump([log_entry], f, indent=2)

