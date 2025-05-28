import os
import json
from warehouse.core import store_snippet

def list_snippets_by_language(language):
    directory = f"snippets/{language}"
    if not os.path.exists(directory):
        print(f"\n⚠️ No snippets found for language: {language}")
        return

    print(f"\n📦 Snippets in '{language}':\n")
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), "r") as file:
                snippet = json.load(file)
                print(f"{filename[:-5]} - {snippet['description']}")
                print(f"   🏷 Tags: {', '.join(snippet['tags'])}")
                print(f"   📅 Created: {snippet['created_at']}\n")

def add_snippet_interactively():
    print("\n📝 Add a New Snippet")
    name = input("Enter snippet name: ").strip()
    language = input("Enter programming language: ").strip().lower()
    description = input("Enter short description: ").strip()
    tags = input("Enter tags (comma-separated): ").strip().split(",")
    code_lines = []
    print("Enter your code (type 'END' on a new line to finish):")
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        code_lines.append(line)
    code = "\n".join(code_lines)

    snippet = store_snippet(name, code, language, tags, description)
    print(f"\n✅ Snippet '{name}' saved successfully to 'snippets/{language}/'!")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. List snippets by language")
    print("2. Add a new snippet")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        lang = input("\nEnter language to list snippets (e.g. python): ").strip().lower()
        list_snippets_by_language(lang)
    elif choice == "2":
        add_snippet_interactively()
    else:
        print("❌ Invalid option selected.")

