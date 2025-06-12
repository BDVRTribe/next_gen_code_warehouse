# run_reverse_string_experiment.py

from phase_4.experiment_runner import run_experiment

def fake_llm(prompt):
    return (
        "Title: Reverse a String\n"
        "Description: Write a Python function that reverses a given string.\n"
        "Tags: ['python', 'string', 'reverse']"
    )

run_experiment(fake_llm)

