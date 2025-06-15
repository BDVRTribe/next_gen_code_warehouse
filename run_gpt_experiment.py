# run_gpt_experiment.py

from phase_4.experiment_runner import run_experiment
from phase_4.gpt_llm import gpt_llm

def custom_llm(_):
    varied_prompt = (
        "Propose a creative AI experiment that does NOT focus on empathy. "
        "Explore fields like robotics, music generation, sustainable AI systems, or AR interfaces."
    )
    return gpt_llm(varied_prompt)

run_experiment(custom_llm)

