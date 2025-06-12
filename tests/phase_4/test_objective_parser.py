import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from phase_4.objective_parser import parse_objective

def test_parse_objective():
    prompt = "Write a Python function that reverses a string"
    result = parse_objective(prompt)

    assert isinstance(result, dict)
    assert result["action"] == "generate_code"
    assert result["language"] == "python"
    assert "reverse" in result["goal_text"].lower()

