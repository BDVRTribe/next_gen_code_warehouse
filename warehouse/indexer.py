import os
import json

SNIPPET_DIR = "snippets"
INDEX_FILE = "index/index.json"

def build_index():
    index = {}

    for language in os.listdir(SNIPPET_DIR):
        lang_path = os.path.join(SNIPPET_DIR, language)
        if not os.path.isdir(lang_path):
            continue

        # ✅ Always initialize each language with an empty dict
        index[language] = {}

        for file in os.listdir(lang_path):
            if file.endswith(".json"):
                filepath = os.path.join(lang_path, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        snippet = json.load(f)
                        lang_key = snippet.get("language", language).lower()
                        snippet_entry = {
                            "filename": file,
                            "language": lang_key,
                            "tags": snippet.get("tags", []),
                            "description": snippet.get("description", ""),
                            "created_by": snippet.get("created_by", ""),
                            "path": filepath,
                            "code": snippet.get("code", "")
                        }
                        index[language][file] = snippet_entry
                except Exception as e:
                    print(f"⚠️ Failed to index {filepath}: {e}")

    # ✅ Ensure index directory exists
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)

    # ✅ Convert nested dict to list for file output
    export_data = {
        lang: list(snippets.values()) for lang, snippets in index.items()
    }

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2)

    print(f"✅ Indexed {sum(len(v) for v in index.values())} snippets into {INDEX_FILE}")
    return index

