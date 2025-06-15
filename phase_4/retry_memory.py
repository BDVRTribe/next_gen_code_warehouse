import json
import os
from phase_4.chamber_core import run_chamber

MEMORY_LOG_FILE = "phase_4/memory_logs/memory.jsonl"

def load_memory(min_score=0.5):
    if not os.path.exists(MEMORY_LOG_FILE):
        print("❌ No memory log found.")
        return []

    with open(MEMORY_LOG_FILE, "r") as f:
        entries = []
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("score", 0.0) >= min_score:
                    entries.append(entry)
            except json.JSONDecodeError:
                continue
    return entries

def select_and_run(entries):
    print("\n📚 Available high-scoring prompts:\n")
    for idx, e in enumerate(entries):
        print(f"{idx+1}. Score: {e['score']:.2f} | Prompt: {e['prompt'][:80]}...")

    try:
        selection = int(input("\nEnter number to retry (0 to cancel): "))
        if selection == 0:
            print("❎ Cancelled.")
            return
        selected_prompt = entries[selection - 1]["prompt"]
        print(f"\n🚀 Retrying chamber for:\n{selected_prompt}")
        run_chamber(selected_prompt)
    except (IndexError, ValueError):
        print("⚠️ Invalid selection.")

if __name__ == "__main__":
    entries = load_memory(min_score=0.5)
    if entries:
        select_and_run(entries)

