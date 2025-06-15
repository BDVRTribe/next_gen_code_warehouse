import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from phase_4.sandbox_runner import run_in_sandbox

def test_run_in_sandbox_success():
    code = "print('Hello, world!')"
    output, error = run_in_sandbox(code)

    assert output == "Hello, world!"
    assert error is None

def test_run_in_sandbox_error():
    code = "raise ValueError('Oops!')"
    output, error = run_in_sandbox(code)

    assert output == ""
    assert "Oops!" in error

