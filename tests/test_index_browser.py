import pytest
from warehouse.index_browser import search_index

sample_index = {
    "python": [
        {
            "filename": "hello_world.json",
            "language": "python",
            "tags": ["basics", "print", "intro"],
            "description": "A simple hello world example.",
            "created_by": "tester"
        },
        {
            "filename": "math_utils.json",
            "language": "python",
            "tags": ["math", "utilities"],
            "description": "Functions for common math operations.",
            "created_by": "tester"
        }
    ]
}

def test_search_by_filename():
    results = search_index(sample_index, "hello")
    assert len(results) == 1
    assert results[0][1]["filename"] == "hello_world.json"

def test_search_by_description():
    results = search_index(sample_index, "math operations")
    assert len(results) == 1
    assert results[0][1]["filename"] == "math_utils.json"

def test_search_by_tag():
    results = search_index(sample_index, "print")
    assert len(results) == 1
    assert results[0][1]["filename"] == "hello_world.json"

def test_search_no_match():
    results = search_index(sample_index, "nonexistent")
    assert len(results) == 0

