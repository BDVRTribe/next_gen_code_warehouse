import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from phase_4.mutation_engine import mutate_code

def test_mutate_code_returns_modified_code():
    original_code = "print('Hello')"
    mutated_code = mutate_code(original_code, feedback="Add exclamation")
    assert isinstance(mutated_code, str)
    assert mutated_code != original_code

