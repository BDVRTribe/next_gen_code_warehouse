import ast

def score_code(code):
    """
    Scores code based on basic metrics: syntax validity and structure.
    Returns a dictionary with 'execution', 'structure', and 'novelty' scores.
    """

    try:
        # Try parsing the code to check for syntax validity
        tree = ast.parse(code)
    except SyntaxError:
        return {
            "execution": 0,
            "structure": 0,
            "novelty": 0
        }

    # Score based on complexity (number of nodes as a proxy)
    node_count = len(list(ast.walk(tree)))
    
    # Simple heuristic: fewer nodes = simpler = lower score
    if node_count < 10:
        structure_score = 3
    elif node_count < 30:
        structure_score = 6
    else:
        structure_score = 9

    # Always mark execution as valid if it parsed successfully
    execution_score = 10

    # Simulate a novelty score using a basic heuristic (can improve later)
    novelty_score = 5 if "lambda" in code or "set" in code else 3

    return {
        "execution": execution_score,
        "structure": structure_score,
        "novelty": novelty_score
    }

