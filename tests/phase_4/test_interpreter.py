# tests/phase_4/test_interpreter.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from phase_4.interpreter import explain_result

def test_explain_result_success():
    result = "42"
    error = None
    score = 1.0
    goal = "Return the answer to life"
    explanation = explain_result(result, error, score, goal)

    assert "successfully" in explanation.lower()
    assert "42" in explanation
    assert "life" in explanation.lower()

def test_explain_result_failure():
    result = None
    error = "NameError: name 'life' is not defined"
    score = 0.2
    goal = "Return the answer to life"
    explanation = explain_result(result, error, score, goal)
     
    assert "error encountered" in explanation.lower()
    assert "nameerror" in explanation.lower()
    assert "life" in explanation.lower()

