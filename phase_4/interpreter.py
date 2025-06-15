# phase_4/interpreter.py

def explain_result(result, error, score, goal):
    """
    Generate a human-readable explanation of what happened in the chamber.
    """
    if score >= 0.9:
        return f"✅ The code successfully fulfilled the goal: '{goal}'. Output was '{result}' with score {score:.2f}."
    elif error:
        return f"❌ Error encountered: {error}. Score: {score:.2f}. Goal was: '{goal}'."
    else:
        return f"⚠️ Output '{result}' did not meet the goal '{goal}'. Score: {score:.2f}."

