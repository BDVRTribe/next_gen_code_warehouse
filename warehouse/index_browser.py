import os
import json
from warehouse.indexer import build_index

INDEX_PATH = "index/index.json"

def load_index():
    if not os.path.exists(INDEX_PATH):
        print("❌ Index file not found. Run `build_index()` first.")
        return {}
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def display_snippets_by_language(index):
    print("\n📚 Snippets by Language:\n")
    for language, snippets in index.items():
        print(f"\n🧠 {language.upper()} — {len(snippets)} snippet(s):")
        for snippet in snippets:
            print(f"  - {snippet['filename']} :: {snippet.get('description', 'No description')}")

def search_index(index, keyword):
    results = []
    keyword_lower = keyword.lower()
    for language, snippets in index.items():
        for snippet in snippets:
            if (keyword_lower in snippet.get("filename", "").lower() or
                keyword_lower in snippet.get("description", "").lower() or
                any(keyword_lower in tag.lower() for tag in snippet.get("tags", []))):
                results.append((language, snippet))
    return results

def run_browser():
    index = load_index()
    if not index:
        return

    while True:
        print("\n[s] Search | [v] View All | [q] Quit")
        cmd = input("Command: ").strip().lower()

        if cmd == "s":
            keyword = input("🔍 Enter search keyword: ").strip()
            results = search_index(index, keyword)
            if results:
                print(f"\n🔎 Found {len(results)} result(s):")
                for lang, snippet in results:
                    print(f"- [{lang}] {snippet['filename']} :: {snippet.get('description', '')}")
            else:
                print("❌ No matches found.")
        elif cmd == "v":
            display_snippets_by_language(index)
        elif cmd == "q":
            print("👋 Exiting index browser.")
            break
        else:
            print("❌ Unknown command.")

if __name__ == "__main__":
    run_browser()

