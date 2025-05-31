import os
import json
from warehouse.core import store_snippet

def test_store_snippet_creates_file():
    # Test values
    name = "test_snippet"
    code = "print('Hello, test!')"
    language = "python"
    tags = ["test", "demo"]
    description = "A test snippet."

    # Run the function
    store_snippet(name, code, language, tags, description, created_by="test_runner")

    # Build expected path
    filename = f"{name.lower().replace(' ', '_')}.json"
    path = os.path.join("snippets", language, filename)

    # Test: check file exists
    assert os.path.exists(path)

# ✅ Add this new test BELOW the one above

def test_delete_snippet(tmp_path, monkeypatch):
    # Setup: Create a mock snippet file in a temp directory
    language = "python"
    snippet_name = "temp_delete_test"
    language_dir = tmp_path / "snippets" / language
    language_dir.mkdir(parents=True)
    snippet_path = language_dir / f"{snippet_name}.json"

    snippet_content = {
        "name": snippet_name,
        "language": language,
        "tags": ["test"],
        "description": "Temporary snippet for deletion test",
        "code": "print('delete me')",
        "created_by": "test",
        "created_at": "2024-01-01T00:00:00Z"
    }

    snippet_path.write_text(json.dumps(snippet_content), encoding="utf-8")

    # Monkeypatch user inputs
    monkeypatch.setattr("builtins.input", lambda _: "1")  # select first snippet
    monkeypatch.setattr("os.path.isdir", lambda path: True)
    monkeypatch.setattr("os.listdir", lambda path: [f"{snippet_name}.json"])
    monkeypatch.setattr("builtins.input", lambda _: "y")  # confirm deletion

    # Patch os.remove to delete the test file
    def mock_remove(path):
        if os.path.exists(path):
            os.remove(path)
    monkeypatch.setattr("os.remove", mock_remove)

    # Import and run
    from warehouse.cli import delete_snippet
    delete_snippet()

    # Test: snippet should be deleted
    assert not snippet_path.exists()

