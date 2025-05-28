from warehouse.core import load_snippets

def list_snippets(language):
    snippets = load_snippets(language)
    if not snippets:
        print(f"No snippets found for language: {language}")
        return

    print(f"\n📦 Snippets in '{language}':\n")
    for idx, snippet in enumerate(snippets, 1):
        print(f"{idx}. {snippet['name']} - {snippet.get('description', 'No description')}")
        print(f"   🏷 Tags: {', '.join(snippet['tags'])}")
        print(f"   📅 Created: {snippet['created_at']}")
        print()

if __name__ == "__main__":
    lang = input("Enter language to list snippets (e.g. python): ").strip()
    list_snippets(lang)

