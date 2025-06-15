# phase_4/interpretability_log.py

from phase_4.analogy_generator import generate_analogy
import json
import os

__all__ = ["load_log", "simplify_explanation", "show_interpretation"]

def load_log(filepath):
    """
    Load a JSON-based interpretability log.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Log file not found: {filepath}")
    
    with open(filepath, 'r') as f:
        return json.load(f)

def simplify_explanation(explanation):
    """
    Simplify an explanation using basic sentence structures.
    """
    if "error" in explanation.lower():
        return "Something went wrong during the code execution."
    elif "success" in explanation.lower():
        return "The code worked as expected."
    else:
        return "Here’s what happened: " + explanation

def show_interpretation(log):
    """
    Display the interpretability details in a readable format.
    """
    print(f"🧠 Goal: {log['goal']}")
    print(f"\n📜 Code:\n{log['code']}")
    print(f"\n📈 Result: {log['result']}")
    print(f"\n🧾 Explanation:\n{simplify_explanation(log['explanation'])}")
    print(f"\n🔍 Analogy:\n{log.get('analogy', 'No analogy provided.')}")

def log_interpretation(goal, code, result, score, explanation, success, path="logs/interpretability.log"):
    """
    Logs detailed interpretation data including an analogy.
    """
    analogy = generate_analogy(goal, result, success)
    log_entry = {
        "goal": goal,
        "code": code,
        "result": result,
        "score": score,
        "explanation": explanation,
        "analogy": analogy
    }

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

