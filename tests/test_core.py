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
    inputs = iter(["python", "1", "y"])  # language, snippet index, confirmation
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("os.path.isdir", lambda path: True)
    monkeypatch.setattr("os.listdir", lambda path: [f"{snippet_name}.json"])

    # Save the original os.remove
    original_remove = os.remove

    # Patch os.remove to delete the test file
    def mock_remove(path):
        path = str(path)  # Ensure compatibility
        if os.path.exists(path):
            original_remove(path)
    monkeypatch.setattr("os.remove", mock_remove)

    # Change working directory to the temp path so CLI works with test file
    os.chdir(tmp_path)

    # Import and run
    from warehouse.cli import delete_snippet
    delete_snippet()

    # Test: snippet should be deleted
    assert not snippet_path.exists()
