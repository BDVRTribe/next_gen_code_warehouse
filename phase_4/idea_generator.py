# phase_4/idea_generator.py

import json
from datetime import datetime

def generate_idea(llm_func):
    """
    Generate an idea using a language model function (llm_func).
    The function should accept a prompt and return text.
    """
    prompt = "Propose an original coding experiment idea for AI research. Include a title, short description, and tags."
    response = llm_func(prompt)

    # Simple parser (expects response to be formatted well)
    idea = {
        "title": "Untitled",
        "description": response.strip(),
        "tags": [],
        "created_at": datetime.now().isoformat()
    }

    return idea

def save_idea(idea, archive_path="idea_archive.json"):
    """
    Save the idea to a local archive file.
    """
    try:
        with open(archive_path, "r") as f:
            archive = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        archive = []

    archive.append(idea)

    with open(archive_path, "w") as f:
        json.dump(archive, f, indent=2)

    print(f"💡 Idea saved to {archive_path}")

