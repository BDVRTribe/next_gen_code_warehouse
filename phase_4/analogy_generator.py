# phase_4/analogy_generator.py

import random

__all__ = ["generate_analogy"]

def generate_analogy(goal, outcome, success):
    if success:
        analogies = [
            f"Like a well-oiled machine, the code smoothly achieved the goal: {goal}.",
            f"The result was like hitting a bullseye — precise and effective.",
            f"Imagine building a bridge, and every plank fits perfectly — that's what this code did for: {goal}."
        ]
    else:
        analogies = [
            f"Trying to {goal} with that code was like using a hammer to fix a watch — not the right tool.",
            f"The outcome missed the point, like baking a cake without turning on the oven.",
            f"Think of asking for a bicycle and getting a unicycle — it moves, but not how you'd expect."
        ]

    return random.choice(analogies)

