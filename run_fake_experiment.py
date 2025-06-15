# run_fake_experiment.py

from phase_4.experiment_runner import run_experiment

# Mock LLM function for offline testing
def mock_llm(prompt):
    return (
        "Title: Print Hello World\n"
        "Description: Generate a Python script that prints 'Hello World'.\n"
        "Tags: ['beginner', 'print', 'hello']"
    )

# Run the experiment with the mock LLM
if __name__ == "__main__":
    run_experiment(mock_llm)

