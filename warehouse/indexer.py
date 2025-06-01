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

        for file in os.listdir(lang_path):
            if file.endswith(".json"):
                filepath = os.path.join(lang_path, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    try:
                        snippet = json.load(f)
                        lang_key = snippet.get("language", language).lower()
                        snippet_entry = {
                            "filename": file,
                            "language": lang_key,
                            "tags": snippet.get("tags", []),
                            "description": snippet.get("description", ""),
                            "created_by": snippet.get("created_by", ""),
                            "path": filepath
                        }
                        index.setdefault(lang_key, []).append(snippet_entry)
                    except Exception as e:
                        print(f"⚠️ Failed to index {filepath}: {e}")

    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    print(f"✅ Indexed {sum(len(v) for v in index.values())} snippets into {INDEX_FILE}")
