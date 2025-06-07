import os
import json
from pathlib import Path
import pytest
import warehouse.indexer as indexer_module

def test_build_index_creates_index_file(tmp_path, monkeypatch):
    # Setup test snippet
    snippet_dir = tmp_path / "snippets" / "python"
    snippet_dir.mkdir(parents=True)
    snippet_path = snippet_dir / "sample_snippet.json"

    snippet_data = {
        "name": "sample_snippet",
        "language": "python",
        "tags": ["example", "test"],
        "description": "Sample snippet for index test",
        "created_by": "tester",
        "code": "print('Hello')"
    }

    snippet_path.write_text(json.dumps(snippet_data), encoding="utf-8")

    # Patch paths
    monkeypatch.setattr(indexer_module, "SNIPPET_DIR", str(tmp_path / "snippets"))
    monkeypatch.setattr(indexer_module, "INDEX_FILE", str(tmp_path / "index" / "index.json"))

    # Run indexing
    index_data = indexer_module.build_index()

    # Check if index file was created
    index_file = tmp_path / "index" / "index.json"
    assert index_file.exists()

    # Load and verify file content
    with open(index_file, "r", encoding="utf-8") as f:
        file_data = json.load(f)

    assert "python" in file_data
    assert any(snip["filename"] == "sample_snippet.json" for snip in file_data["python"])

    # Validate return structure
    assert isinstance(index_data, dict)
    assert "python" in index_data
    assert "sample_snippet.json" in index_data["python"]
    assert index_data["python"]["sample_snippet.json"]["language"] == "python"

def test_build_index_skips_malformed_json(tmp_path, monkeypatch, capsys):
    # Setup valid snippet
    valid_dir = tmp_path / "snippets" / "python"
    valid_dir.mkdir(parents=True)

    valid_snippet = {
        "name": "good_snippet",
        "language": "python",
        "tags": [],
        "description": "A valid snippet",
        "created_by": "tester",
        "code": "print('ok')"
    }

    (valid_dir / "valid.json").write_text(json.dumps(valid_snippet), encoding="utf-8")

    # Malformed JSON file
    (valid_dir / "broken.json").write_text("{ bad json", encoding="utf-8")

    # Patch paths
    monkeypatch.setattr(indexer_module, "SNIPPET_DIR", str(tmp_path / "snippets"))
    monkeypatch.setattr(indexer_module, "INDEX_FILE", str(tmp_path / "index" / "index.json"))

    # Run indexer
    index_data = indexer_module.build_index()

    # Assertions
    assert "python" in index_data
    assert "valid.json" in index_data["python"]
    assert "broken.json" not in index_data["python"]

    # Check console output
    captured = capsys.readouterr()
    assert "⚠️ Failed to index" in captured.out

def test_build_index_handles_empty_language_folder(tmp_path, monkeypatch):
    # Create empty language folder
    empty_lang_dir = tmp_path / "snippets" / "ruby"
    empty_lang_dir.mkdir(parents=True)

    # Patch paths
    monkeypatch.setattr(indexer_module, "SNIPPET_DIR", str(tmp_path / "snippets"))
    monkeypatch.setattr(indexer_module, "INDEX_FILE", str(tmp_path / "index" / "index.json"))

    # Run
    index_data = indexer_module.build_index()

    # Assert the empty folder is still represented
    assert "ruby" in index_data
    assert isinstance(index_data["ruby"], dict)
    assert index_data["ruby"] == {}

    # Load from file
    index_file = tmp_path / "index" / "index.json"
    assert index_file.exists()
    file_data = json.loads(index_file.read_text(encoding="utf-8"))

    assert "ruby" in file_data
    assert isinstance(file_data["ruby"], list)
    assert file_data["ruby"] == []

