# phase_4/memory_logger.py

import os
import json
from datetime import datetime

MEMORY_LOG_PATH = "phase_4/memory_logs"
os.makedirs(MEMORY_LOG_PATH, exist_ok=True)

def log_memory(prompt, generation_num, code, error=None, score=None):
    timestamp = datetime.utcnow().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "generation": generation_num,
        "prompt": prompt,
        "code": code,
        "error": error,
        "score": score
    }

    log_file = os.path.join(MEMORY_LOG_PATH, "memory.jsonl")
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


