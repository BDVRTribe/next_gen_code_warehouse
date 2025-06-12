# tests/phase_4/test_experiment_runner.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from phase_4.experiment_runner import run_experiment

def mock_llm(prompt):
    return (
        "Title: Test Echo Prompt\n"
        "Description: Write a Python function that echoes input.\n"
        "Tags: ['test', 'echo', 'basic']"
    )

def test_run_experiment():
    result = run_experiment(llm=mock_llm)
    assert "title" in result
    assert "prompt" in result
    assert "final_code" in result
    assert "duration_sec" in result

