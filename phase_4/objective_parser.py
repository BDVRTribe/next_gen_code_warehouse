# phase_4/objective_parser.py

def parse_objective(prompt):
    """
    Very basic parser that returns a structured dictionary.
    Later this can be expanded with NLP.
    """
    return {
        "action": "generate_code",
        "language": "python",
        "goal_text": prompt.strip()
    }

