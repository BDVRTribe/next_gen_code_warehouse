import json
import os

MEMORY_LOG_FILE = "phase_4/memory_logs/memory.jsonl"

def list_memory_entries(min_score=0.0):
    if not os.path.exists(MEMORY_LOG_FILE):
        print("❌ No memory log file found.")
        return

    with open(MEMORY_LOG_FILE, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        try:
            entry = json.loads(line)
            score = entry.get("score", 0.0)
            if score >= min_score:
                print(f"\n🔢 Entry #{i+1}")
                print(f"🕒 Timestamp: {entry.get('timestamp')}")
                print(f"📈 Score: {score}")
                print(f"🧪 Generation: {entry.get('generation')}")
                print(f"💬 Prompt: {entry.get('prompt')[:60]}...")
                print(f"💻 Code: {entry.get('code')[:80]}...")
        except json.JSONDecodeError:
            print(f"⚠️ Failed to parse entry #{i+1}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="View memory log entries.")
    parser.add_argument("--min_score", type=float, default=0.0, help="Minimum score to show")
    args = parser.parse_args()

    list_memory_entries(min_score=args.min_score)

