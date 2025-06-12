# phase_4/mutation_engine.py

def mutate_code(code, feedback=""):
    """
    Mutates the provided code based on feedback.
    If the code is None (e.g., generation failed), return a placeholder.

    Args:
        code (str or None): The code to mutate.
        feedback (str): Feedback or error message to guide mutation.

    Returns:
        str: Mutated version of the code or a placeholder message.
    """
    if code is None:
        return "# No code to mutate due to prior error or empty generation."

    # Basic mutation placeholder (can be enhanced with actual logic later)
    mutated = "# Modified code based on feedback\n" + code + "\n# End mutation"
    return mutated

