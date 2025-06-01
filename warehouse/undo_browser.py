import os
import json
import glob
from warehouse.core import restore_snapshot

UNDO_DIR = "undo_logs"
ITEMS_PER_PAGE = 10  # Adjustable pagination size

def load_undo_logs():
    logs = sorted(glob.glob(os.path.join(UNDO_DIR, "*.json")), reverse=True)
    entries = []
    for log in logs:
        try:
            with open(log, "r", encoding="utf-8") as f:
                data = json.load(f)
                entries.append((log, data))
        except Exception as e:
            print(f"⚠️ Failed to load {log}: {e}")
    return entries

def filter_entries(entries, action_filter=None, keyword=None):
    filtered = []
    for path, entry in entries:
        action = entry.get("action_type", "").upper()
        filename = entry.get("filename", "").lower()
        if action_filter and action != action_filter.upper():
            continue
        if keyword and keyword.lower() not in filename:
            continue
        filtered.append((path, entry))
    return filtered

def display_page(entries, page):
    os.system('clear' if os.name == 'posix' else 'cls')
    total = len(entries)
    start = (page - 1) * ITEMS_PER_PAGE
    end = min(start + ITEMS_PER_PAGE, total)
    
    print(f"\n🕑 Undo Log Entries ({start + 1}–{end} of {total}):\n")
    for i, (log_path,_
