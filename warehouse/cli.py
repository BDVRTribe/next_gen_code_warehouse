import os
import json
from datetime import datetime
from warehouse.core import store_snippet
from warehouse.validator import validate_snippet
from warehouse.indexer import build_index
from warehouse.logger import log_event
from warehouse.core import undo_last_action


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
    tags = [tag.strip() for tag in input("Enter tags (comma-separated): ").strip().split(",")]
    code_lines = []
    print("Enter your code (type 'END' on a new line to finish):")
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        code_lines.append(line)
    code = "\n".join(code_lines)

    snippet = {
        "name": name,
        "language": language,
        "tags": tags,
        "description": description,
        "code": code,
        "created_by": "CLI",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    valid, message = validate_snippet(snippet)
    if not valid:
        print(f"\n❌ Snippet not saved: {message}")
        return

    store_snippet(name, code, language, tags, description)
    log_event("add", name, language, {"description": description, "tags": tags})
    print(f"\n✅ Snippet '{name}' saved successfully to 'snippets/{language}/'!")

def update_snippet():
    language = input("Enter language of the snippet to update: ").strip().lower()
    language_dir = os.path.join("snippets", language)

    if not os.path.isdir(language_dir):
        print(f"No snippets found for language: {language}")
        return

    files = [f for f in os.listdir(language_dir) if f.endswith(".json")]
    if not files:
        print(f"No snippets to update in {language}")
        return

    print(f"\n🛠️ Available snippets in '{language}':")
    for i, filename in enumerate(files, 1):
        print(f"{i}. {filename}")

    choice = input("Enter number of snippet to update: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(files)):
        print("Invalid selection.")
        return

    selected_file = files[int(choice) - 1]
    file_path = os.path.join(language_dir, selected_file)

    with open(file_path, "r") as file:
        snippet = json.load(file)

    print("\nPress Enter to keep existing values.")
    new_name = input(f"Name [{snippet['name']}]: ").strip() or snippet["name"]
    new_description = input(f"Description [{snippet['description']}]: ").strip() or snippet["description"]
    new_tags = input(f"Tags (comma-separated) [{', '.join(snippet['tags'])}]: ").strip()
    new_code_lines = []
    print("Enter new code (or type END to keep existing):")
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        new_code_lines.append(line)

    if new_tags:
        snippet["tags"] = [tag.strip() for tag in new_tags.split(",")]
    if new_code_lines:
        snippet["code"] = "\n".join(new_code_lines)

    snippet["name"] = new_name
    snippet["description"] = new_description

    valid, message = validate_snippet(snippet)
    if not valid:
        print(f"\n❌ Snippet not updated: {message}")
        return

    with open(file_path, "w") as file:
        json.dump(snippet, file, indent=4)

    print(f"✅ Snippet '{new_name}' updated successfully.")
    log_event("update", new_name, language, {"tags": snippet["tags"]})

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
        log_event("delete", selected_file.replace(".json", ""), language)
    else:
        print("❌ Deletion canceled.")

def search_snippets_by_tag():
    tag_input = input("Enter tag to search (e.g. math): ").strip().lower()
    found = False

    print(f"\n🔎 Searching for snippets with tag '{tag_input}'...\n")

    snippets_dir = "snippets"
    for language in os.listdir(snippets_dir):
        lang_dir = os.path.join(snippets_dir, language)
        if not os.path.isdir(lang_dir):
            continue
        for file in os.listdir(lang_dir):
            if file.endswith(".json"):
                path = os.path.join(lang_dir, file)
                with open(path, "r") as f:
                    try:
                        snippet = json.load(f)
                        tags = [t.lower() for t in snippet.get("tags", [])]
                        if tag_input in tags:
                            found = True
                            print(f"{snippet['name']} ({language}) - {snippet['description']}")
                            print(f"   🏷 Tags: {', '.join(snippet['tags'])}")
                            print(f"   📅 Created: {snippet['created_at']}\n")
                    except json.JSONDecodeError:
                        continue

    if not found:
        print("⚠️ No snippets found with that tag.")

def rebuild_global_index():
    print("\n📦 Rebuilding global index...")
    build_index()
    print("✅ Index rebuilt successfully.")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. List snippets by language")
    print("2. Add a new snippet")
    print("3. Delete a snippet")
    print("4. Update a snippet")
    print("5. Rebuild global index")
    print("6. Search snippets by tag")
    print("7. Undo last action")


    choice = input("Enter 1–6: ").strip()

    if choice == "1":
        lang = input("\nEnter language to list snippets (e.g. python): ").strip().lower()
        list_snippets_by_language(lang)
    elif choice == "2":
        add_snippet_interactively()
    elif choice == "3":
        delete_snippet()
    elif choice == "4":
        update_snippet()
    elif choice == "5":
        rebuild_global_index()
    elif choice == "6":
        search_snippets_by_tag()
    elif choice == "7":
        print("\n⏪ Rolling back last action...")
        undo_last_action()
        print("✅ Undo complete!\n")

    else:
        print("❌ Invalid option selected.")
