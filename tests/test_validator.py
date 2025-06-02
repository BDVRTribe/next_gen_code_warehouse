from warehouse.validator import validate_snippet

def test_valid_snippet_passes():
    valid_snippet = {
        "name": "valid_snippet",
        "language": "python",
        "tags": ["example", "test"],
        "description": "A test snippet for validation.",
        "code": "print('Hello')",
        "created_by": "tester",
        "created_at": "2024-01-01T00:00:00Z"
    }
    is_valid, message = validate_snippet(valid_snippet)
    assert is_valid, message  # Optional: show message if it fails again

def test_invalid_snippet_fails_missing_fields():
    invalid_snippet = {
        "name": "invalid_snippet",
        "language": "python",
        "code": "print('Oops')"  # Missing tags, description, created_by, created_at
    }
    is_valid, message = validate_snippet(invalid_snippet)
    assert not is_valid
    assert "Missing required fields" in message

def test_invalid_tags_format():
    bad_tags = {
        "name": "bad_tags",
        "language": "python",
        "tags": "notalist",
        "description": "Tags is not a list.",
        "code": "print('Oops')",
        "created_by": "tester",
        "created_at": "2024-01-01T00:00:00Z"
    }
    is_valid, message = validate_snippet(bad_tags)
    assert not is_valid
    assert "'tags' must be a list." in message

def test_invalid_date_format():
    bad_date = {
        "name": "bad_date",
        "language": "python",
        "tags": ["example"],
        "description": "Bad date format.",
        "code": "print('Oops')",
        "created_by": "tester",
        "created_at": "01-01-2024"  # Invalid format
    }
    is_valid, message = validate_snippet(bad_date)
    assert not is_valid
    assert "'created_at' is not in ISO 8601 format." in message

def test_invalid_python_syntax():
    bad_syntax = {
        "name": "bad_syntax",
        "language": "python",
        "tags": ["error"],
        "description": "Invalid Python code.",
        "code": "def bad(:",
        "created_by": "tester",
        "created_at": "2024-01-01T00:00:00Z"
    }
    is_valid, message = validate_snippet(bad_syntax)
    assert not is_valid
    assert "Python syntax error" in message

