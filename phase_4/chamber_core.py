# phase_4/chamber_core.py

__all__ = ["run_chamber"]

from phase_4.memory_logger import log_memory
from phase_4.interpretability_log import log_interpretation
from phase_4.interpreter import explain_result
from phase_4.objective_parser import parse_objective
from phase_4.code_synthesizer import generate_code
from phase_4.sandbox_runner import run_in_sandbox
from phase_4.feedback_evaluator import evaluate_result
from phase_4.mutation_engine import mutate_code
from phase_4.fitness_tracker import log_generation
from phase_4.feedback_engine import FeedbackEngine

MAX_ITERATIONS = 5
SUCCESS_THRESHOLD = 0.9

def run_chamber(prompt):
    goal = parse_objective(prompt)
    feedback_engine = FeedbackEngine()

    previous_error = None
    previous_code = None

    try:
        for generation in range(MAX_ITERATIONS):
            print(f"\n🔁 Generation {generation + 1}")
            code = generate_code(goal, previous_error=previous_error, previous_code=previous_code)
            if not code:
                break

            result, error = run_in_sandbox(code)
            score = evaluate_result(result, error, goal)

            explanation = explain_result(result, error, score, goal)
            print(explanation)

            log_interpretation(goal, code, result, score, explanation, score >= SUCCESS_THRESHOLD)
            log_generation(generation, code, result, score)
            log_memory(prompt, generation, code, error, score)

            if score >= SUCCESS_THRESHOLD:
                print("✅ Chamber Success! Final Code:")
                print(code)
                return code

            previous_error = error
            previous_code = code

            action = feedback_engine.feedback(goal, result, error, score)

            if action == "mutate":
                code = mutate_code(code, feedback=error)
            else:
                print(f"⚠️ Unknown action '{action}', defaulting to mutate.")
                code = mutate_code(code, feedback=error)

    except KeyboardInterrupt:
        print("\n🟥 Chamber manually stopped by user.")
        return None

    print("❌ Chamber failed to reach threshold.")
    return None

