def evaluate_result(result, error, goal):
    """
    Assigns a score based on result quality.
    """
    if error:
        return 0.0

    prompt = goal.get("goal_text", "").lower()
    score = 0.0

    if "reverse" in prompt and "string" in prompt:
        if result and result.strip() == "stressed":  # reverse of 'desserts'
            score = 1.0
        else:
            score = 0.5

    elif "print" in prompt and "hello" in prompt:
        if result and "hello world" in result.lower():
            score = 1.0
        else:
            score = 0.5

    return score

