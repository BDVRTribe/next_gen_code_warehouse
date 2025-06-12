import os
import json

output_file = "all_snippets_dump.txt"
snippets_dir = "snippets/python"

with open(output_file, "w") as out:
    for filename in sorted(os.listdir(snippets_dir)):
        if filename.endswith(".json"):
            path = os.path.join(snippets_dir, filename)
            with open(path, "r") as f:
                data = json.load(f)
                out.write(f"📄 File: {filename}\n")
                out.write(f"Title: {data.get('title')}\n")
                out.write(f"Description: {data.get('description')}\n")
                out.write("Code:\n")
                out.write(data.get("code", "") + "\n")
                out.write("-" * 60 + "\n\n")
print(f"\n✅ Exported to {output_file}")

