# phase_4/chamber_core.py

__all__ = ["run_chamber"]

from phase_4.objective_parser import parse_objective
from phase_4.code_synthesizer import generate_code
from phase_4.sandbox_runner import run_in_sandbox
from phase_4.feedback_evaluator import evaluate_result
from phase_4.mutation_engine import mutate_code
from phase_4.fitness_tracker import log_generation

MAX_ITERATIONS = 5
SUCCESS_THRESHOLD = 0.9

def run_chamber(prompt):
    goal = parse_objective(prompt)

    for generation in range(MAX_ITERATIONS):
        print(f"\n🔁 Generation {generation + 1}")
        code = generate_code(goal)
        result, error = run_in_sandbox(code)
        score = evaluate_result(result, error, goal)

        log_generation(generation, code, result, score)

        if score >= SUCCESS_THRESHOLD:
            print("✅ Chamber Success! Final Code:")
            print(code)
            return code

        code = mutate_code(code, feedback=error)

    print("❌ Chamber failed to reach threshold.")
    return None

