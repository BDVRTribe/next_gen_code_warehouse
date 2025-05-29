import os
import json
from warehouse.core import store_snippet
from warehouse.validator import validate_snippet

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

    # Validate the saved snippet
    snippet_path = f"snippets/{language}/{name.replace(' ', '_')}.json"
    print("\n🔍 Validating saved snippet...")
    validate_snippet_file(snippet_path)

def delete_snippet():
    language = input("Enter language of the snippet to delete: ").strip()
    language_dir = os.path.join("snippets", language)

    if not os.path.isdir(language_dir):
        print(f"No snippets found for language: {language}")
        return

    files = [f for f in os.listdir(language_dir) if f.endswith(".json")]
    if not files:
        print(f"No snippets to delete in {language}")
        return

    print(f"\n🗑️ Available snippets in '{language}':")
    for i, filename in enumerate(files, 1):
        print(f"{i}. {filename}")

    choice = input("Enter number of snippet to delete: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(files)):
        print("Invalid selection.")
        return

    selected_file = files[int(choice) - 1]
    confirm = input(f"Are you sure you want to delete '{selected_file}'? (y/N): ").strip().lower()
    if confirm == 'y':
        os.remove(os.path.join(language_dir, selected_file))
        print(f"✅ Deleted {selected_file}")
    else:
        print("❌ Deletion canceled.")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. List snippets by language")
    print("2. Add a new snippet")
    print("3. Delete a snippet")
    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        lang = input("\nEnter language to list snippets (e.g. python): ").strip().lower()
        list_snippets_by_language(lang)
    elif choice == "2":
        add_snippet_interactively()
    elif choice == "3":
        delete_snippet()
    else:
        print("❌ Invalid option selected.")
