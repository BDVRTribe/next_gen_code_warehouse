import json
import os
from datetime import datetime

LOG_FILE = "logs/activity.log"

def log_event(action, name, language=None, details=None):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "name": name,
        "language": language,
        "details": details or {}
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

