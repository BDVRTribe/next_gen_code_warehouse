import os
import json
from pathlib import Path
import warehouse.core as core_module
from warehouse.core import store_snippet

def test_store_snippet_creates_file(tmp_path, monkeypatch):
    # Setup isolated environment
    test_dir = tmp_path / "snippets" / "python"
    monkeypatch.setattr(core_module, "SNIPPET_DIR", str(tmp_path / "snippets"))

    # Test values
    name = "test_snippet"
    code = "print('Hello, test!')"
    language = "python"
    tags = ["test", "demo"]
    description = "A test snippet."

    # Run the function
    store_snippet(name, code, language, tags, description, created_by="test_runner")

    # Expected file path
    filename = f"{name.lower().replace(' ', '_')}.json"
    path = test_dir / filename

    # Test: check file exists
    assert path.exists()

    # Test: check file content
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    assert data["name"] == name
    assert data["language"] == language
    assert data["tags"] == tags
    assert data["description"] == description
    assert data["code"] == code
    assert data["created_by"] == "test_runner"
    assert "created_at" in data

