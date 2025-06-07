import os
import json
import subprocess
from datetime import datetime
from warehouse.core import store_snippet
from warehouse.validator import validate_snippet
from warehouse.indexer import build_index
from warehouse.logger import log_event, log_undo_action
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
    language = input("Enter language of the snippet to delete: ").strip().lower()
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
    file_path = os.path.join(language_dir, selected_file)

    confirm = input(f"Are you sure you want to delete '{selected_file}'? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Deletion canceled.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            snapshot_before = json.load(f)
    except Exception as e:
        print(f"⚠️ Could not load snippet for undo logging: {e}")
        snapshot_before = None

    log_undo_action(
        action_type="delete",
        language=language,
        filename=selected_file,
        snapshot_before=snapshot_before
    )

    os.remove(file_path)
    print(f"✅ Deleted {selected_file}")
    log_event("delete", selected_file.replace(".json", ""), language)

def search_snippets_by_tag():
    tag_input = input("Enter tag to search (e.g. math): ").strip().lower()
    index_file = "index/index.json"

    if not os.path.exists(index_file):
        print("⚠️ Index not found. Please rebuild the index first.")
        return

    with open(index_file, "r", encoding="utf-8") as f:
        try:
            snippets = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Index file is corrupted or unreadable.")
            return

    matches = []
    for lang_snippets in snippets.values():
        for snippet in lang_snippets:
            tags = [tag.lower() for tag in snippet.get("tags", [])]
            if tag_input in tags:
                matches.append(snippet)

    if not matches:
        print(f"❌ No snippets found with tag '{tag_input}'")
        return

    print(f"\n🔎 Found {len(matches)} snippet(s) with tag '{tag_input}':\n")
    for snip in matches:
        print(f"{snip['name']} ({snip['language']}) - {snip['description']}")
        print(f"   🏷 Tags: {', '.join(snip.get('tags', []))}")
        print(f"   👤 By: {snip.get('created_by', 'unknown')}")
        print(f"   📁 File: {snip['path']}\n")

def rebuild_global_index():
    print("\n📦 Rebuilding global index...")
    build_index()
    print("✅ Index rebuilt successfully.")

def launch_undo_gui():
    subprocess.run(["python3", "undo_browser.py"])

if __name__ == "__main__":
    print("Choose an option:")
    print("1. List snippets by language")
    print("2. Add a new snippet")
    print("3. Delete a snippet")
    print("4. Update a snippet")
    print("5. Rebuild global index")
    print("6. Search snippets by tag")
    print("7. Undo last action")
    print("8. Launch Undo Snapshot Browser")

    choice = input("Enter 1–8: ").strip()

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
    elif choice == "8":
        print("\n🚀 Launching Undo Snapshot Browser...")
        launch_undo_gui()
    else:
        print("❌ Invalid option selected.")

