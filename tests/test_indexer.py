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
        "created_by": "tester"
    }

    snippet_path.write_text(json.dumps(snippet_data), encoding="utf-8")

    # Patch paths
    monkeypatch.setattr(indexer_module, "SNIPPET_DIR", str(tmp_path / "snippets"))
    monkeypatch.setattr(indexer_module, "INDEX_FILE", str(tmp_path / "index" / "index.json"))

    # Run indexing
    indexer_module.build_index()

    # Check if index file was created
    index_file = tmp_path / "index" / "index.json"
    assert index_file.exists()

    # Load and verify content
    with open(index_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "python" in data
    assert len(data["python"]) == 1
    assert data["python"][0]["name"] == "sample_snippet"
    assert data["python"][0]["language"] == "python"

