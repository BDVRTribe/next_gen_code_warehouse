import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from unittest.mock import patch
from phase_4.chamber_core import run_chamber

@patch('phase_4.mutation_engine.mutate_code')
@patch('phase_4.chamber_core.log_generation')  # ✅ patching where it’s used
@patch('phase_4.feedback_evaluator.evaluate_result')
@patch('phase_4.sandbox_runner.run_in_sandbox')
@patch('phase_4.code_synthesizer.generate_code')
@patch('phase_4.objective_parser.parse_objective')
def test_run_chamber_success(mock_parse, mock_gen, mock_run, mock_eval, mock_log, mock_mutate):
    mock_parse.return_value = "reverse_string_goal"
    mock_gen.return_value = "print('Hello World')"
    mock_run.return_value = ("desserts", None)
    mock_eval.return_value = 1.0

    result = run_chamber("Reverse a string")

    assert result is not None
    mock_log.assert_called()
    mock_mutate.assert_not_called()

