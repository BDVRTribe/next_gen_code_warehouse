# tests/phase_4/test_analogy_generator.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from phase_4.analogy_generator import generate_analogy

def test_generate_analogy_success():
    analogy = generate_analogy("Solve a maze", "Found the exit", True)
    assert "like" in analogy.lower() or "as if" in analogy.lower()

def test_generate_analogy_failure():
    analogy = generate_analogy("Solve a maze", "Got stuck", False)
    assert "like" in analogy.lower() or "as if" in analogy.lower()

