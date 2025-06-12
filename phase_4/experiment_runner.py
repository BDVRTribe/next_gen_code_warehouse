# phase_4/experiment_runner.py

import time
from datetime import datetime, timezone
from phase_4.idea_generator import generate_idea
from phase_4.chamber_core import run_chamber

__all__ = ["run_experiment"]

def run_experiment(llm=None):
    idea = generate_idea(llm)
    prompt = idea["description"]

    print(f"\n🧪 Running experiment: {idea['title']}")
    print(f"📝 Prompt: {prompt}")
    print(f"🕒 Started at: {datetime.now(timezone.utc).isoformat()}")

    start_time = time.time()
    final_code = run_chamber(prompt)
    duration = time.time() - start_time

    experiment_result = {
        "title": idea["title"],
        "prompt": prompt,
        "final_code": final_code,
        "duration_sec": round(duration, 2),
        "created_at": idea["created_at"],
    }

    print(f"\n📊 Experiment Complete in {experiment_result['duration_sec']}s")
    return experiment_result


