import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from phase_4.feedback_evaluator import evaluate_result

def test_score_success():
    goal = {"goal_text": "Reverse a string"}
    result = "desserts"
    error = None

    score = evaluate_result(result, error, goal)
    assert score == 1.0

def test_score_partial():
    goal = {"goal_text": "Reverse a string"}
    result = "something wrong"
    error = None

    score = evaluate_result(result, error, goal)
    assert score == 0.5

def test_score_failure():
    goal = {"goal_text": "Reverse a string"}
    result = ""
    error = "NameError"

    score = evaluate_result(result, error, goal)
    assert score == 0.0

