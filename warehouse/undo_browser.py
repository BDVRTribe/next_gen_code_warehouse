import os
import json
from datetime import datetime
from warehouse.core import restore_snapshot

UNDO_LOG_PATH = "logs/undo_log.jsonl"

def browse_undo_log():
    if not os.path.exists(UNDO_LOG_PATH):
        print("⚠️ Undo log is empty or missing.")
        return

    with open(UNDO_LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        print("⚠️ No undo actions found.")
        return

    actions = [json.loads(line) for line in lines]
    actions.reverse()  # Show latest first

    print("\n📜 Undo History:\n")
    for idx, action in enumerate(actions):
        timestamp = action.get("timestamp", "unknown")
        filename = action.get("filename", "unknown")
        lang = action.get("language", "unknown")
        print(f"{idx+1}. [{timestamp}] {action['action_type'].upper()} - {filename} ({lang})")

    choice = input("\nSelect entry number to inspect or [Q] to quit: ").strip().lower()
    if choice == 'q':
        return
    if not choice.isdigit() or not (1 <= int(choice) <= len(actions)):
        print("❌ Invalid selection.")
        return

    selected = actions[int(choice) - 1]
    print("\n🧐 Entry Details:")
    print(json.dumps(selected, indent=2))

    confirm = input("\n⏪ Reapply this undo action? (y/N): ").strip().lower()
    if confirm == "y":
        restore_snapshot(selected)
        print("✅ Action reapplied.")
    else:
        print("❌ Action not reapplied.")

