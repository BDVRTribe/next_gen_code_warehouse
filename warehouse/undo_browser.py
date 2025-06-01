import os
import json
import glob
from warehouse.core import restore_snapshot

UNDO_DIR = "undo_logs"

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

def display_undo_options(entries):
    print("\n🕑 Undo Log Entries:\n")
    for i, (log_path, data) in enumerate(entries, 1):
        name = data.get("filename", "unknown")
        action = data.get("action_type", "unknown")
        language = data.get("language", "unknown")
        print(f"{i}. [{action.upper()}] {name} ({language})")

def prompt_selection(count):
    choice = input(f"\nSelect a snapshot to restore (1–{count}) or 'q' to quit: ").strip()
    if choice.lower() == "q":
        return None
    if not choice.isdigit() or not (1 <= int(choice) <= count):
        print("❌ Invalid choice.")
        return None
    return int(choice) - 1

def run_browser():
    if not os.path.exists(UNDO_DIR):
        print("❌ No undo logs directory found.")
        return

    entries = load_undo_logs()
    if not entries:
        print("❌ No undo logs found.")
        return

    display_undo_options(entries)
    index = prompt_selection(len(entries))
    if index is None:
        return

    selected_path, action = entries[index]
    confirm = input(f"\nAre you sure you want to restore '{action.get('filename')}'? (y/N): ").strip().lower()
    if confirm == "y":
        restore_snapshot(action)
    else:
        print("❌ Restore cancelled.")

if __name__ == "__main__":
    run_browser()
