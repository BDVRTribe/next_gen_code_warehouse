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
    for i, (log_path, data) in enumerate(entries[start:end], start=start + 1):
        name = data.get("filename", "unknown")
        action = data.get("action_type", "unknown")
        language = data.get("language", "unknown")
        print(f"{i}. [{action.upper()}] {name} ({language})")

def prompt_selection(entries):
    choice = input(f"\nSelect a snapshot to restore (1–{len(entries)}) or 'q' to quit: ").strip()
    if choice.lower() == "q":
        return None
    if not choice.isdigit():
        print("❌ Invalid input.")
        return None
    idx = int(choice) - 1
    if not (0 <= idx < len(entries)):
        print("❌ Choice out of range.")
        return None
    return idx

def run_browser():
    if not os.path.exists(UNDO_DIR):
        print("❌ No undo logs directory found.")
        return

    all_entries = load_undo_logs()
    print(f"🔍 DEBUG: Loaded {len(all_entries)} undo log entries.")  # Debug line
    filtered_entries = all_entries
    current_page = 1

    while True:
        if not filtered_entries:
            print("❌ No matching entries.")
            return

        display_page(filtered_entries, current_page)
        print("\n[n] Next page | [p] Prev page | [f] Filter | [r] Reset filters | [q] Quit")
        cmd = input("Command or number: ").strip().lower()

        if cmd == "n":
            if current_page * ITEMS_PER_PAGE < len(filtered_entries):
                current_page += 1
            else:
                print("⚠️ No more pages.")
        elif cmd == "p":
            if current_page > 1:
                current_page -= 1
            else:
                print("⚠️ Already at first page.")
        elif cmd == "f":
            act = input("Filter by action (ADD/EDIT/DELETE or leave blank): ").strip()
            kw = input("Filter by filename keyword or leave blank: ").strip()
            filtered_entries = filter_entries(all_entries, act, kw)
            current_page = 1
            print(f"🔍 DEBUG: Filtered down to {len(filtered_entries)} entries.")
        elif cmd == "r":
            filtered_entries = all_entries
            current_page = 1
            print("🔄 Filters reset.")
        elif cmd == "q":
            print("👋 Exiting undo browser.")
            break
        elif cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < len(filtered_entries):
                selected_path, action = filtered_entries[idx]
                confirm = input(f"\n⚠️ Restore '{action.get('filename')}'? (y/N): ").strip().lower()
                if confirm == "y":
                    restore_snapshot(action)
                    break
                else:
                    print("❌ Restore cancelled.")
            else:
                print("❌ Index out of bounds.")
        else:
            print("❌ Unknown command.")

if __name__ == "__main__":
    run_browser()
