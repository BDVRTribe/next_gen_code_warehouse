# tests/phase_4/test_interpretability_log.py

import os
import json
from phase_4.interpretability_log import load_log, simplify_explanation, show_interpretation

# Setup test log file content
test_log = {
    "goal": "Reverse a string",
    "code": "print('desserts'[::-1])",
    "result": "stressed",
    "explanation": "✅ Success! The code correctly reversed the string.",
    "analogy": "It's like reading a word backwards in a mirror."
}

def test_simplify_explanation():
    assert "worked" in simplify_explanation(test_log["explanation"]).lower()

def test_load_log(tmp_path):
    test_file = tmp_path / "log.json"
    test_file.write_text(json.dumps(test_log))
    loaded = load_log(test_file)
    assert loaded["goal"] == "Reverse a string"

def test_show_interpretation(capsys):
    show_interpretation(test_log)
    captured = capsys.readouterr()
    assert "Reverse a string" in captured.out
    assert "desserts" in captured.out

