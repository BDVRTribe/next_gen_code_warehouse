# run_custom_experiment.py

from phase_4.experiment_runner import run_experiment

def file_based_llm(_):
    try:
        with open("prompt.txt", "r") as f:
            prompt = f.read().strip()
            print("📥 Loaded prompt from prompt.txt:\n")
            print(prompt)
            return prompt
    except FileNotFoundError:
        print("❌ 'prompt.txt' not found. Please create it in the project root.")
        return ""

run_experiment(file_based_llm)

