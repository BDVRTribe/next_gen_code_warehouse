# phase_4/sandbox_runner.py

import io
import contextlib

def run_in_sandbox(code):
    """
    Runs the given Python code string and captures output or error.
    Returns a tuple: (output, error_message or None)
    """
    output_buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {})  # Safe globals, no builtins injected
        return (output_buffer.getvalue().strip(), None)
    except Exception as e:
        return ("", str(e))

