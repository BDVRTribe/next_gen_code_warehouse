import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from phase_4.code_synthesizer import generate_code

def test_generate_code_reverse_string():
    goal = {
        "goal_text": "Write a function that reverses a string"
    }

    code = generate_code(goal)

    assert "def reverse_string" in code
    assert "return s[::-1]" in code

def test_generate_code_default():
    goal = {
        "goal_text": "Just do something random"
    }

    code = generate_code(goal)

    assert "def example_function" in code
    assert "placeholder" in code

