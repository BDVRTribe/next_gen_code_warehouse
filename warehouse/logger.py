import json
import os
from datetime import datetime, timezone

LOG_FILE = "logs/activity.log"

def log_event(action, name, language=None, details=None):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "name": name,
        "language": language,
        "details": details or {}
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def log_undo_action(action_type, language, filename, snapshot_before=None):
    undo_log = {
        "action_type": action_type,
        "language": language,
        "filename": filename,
        "snapshot_before": snapshot_before,
        "timestamp": datetime.now(timezone.utc).isoformat(),


    }

    os.makedirs("undo_logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    log_filename = f"undo_logs/{timestamp}.json"

    with open(log_filename, "w") as f:
        json.dump(undo_log, f, indent=2)


