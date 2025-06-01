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

