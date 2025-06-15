import os
import random
from string import Template
from warehouse.prompt_engine import get_prompt
from warehouse.executor import execute_code, clean_code
from warehouse.logger import log_event, log_memory_entry
from warehouse.evaluator import score_code
from warehouse.core import store_snippet

# Prompt template
PROMPT_TEMPLATE = Template(
    "You are an expert Python programmer.\n"
    "Task Level: $level (5=beginner, 0=revolutionary)\n\n"
    "Instructions:\n$instructions\n\n"
    "Goal:\n$goal\n\n"
    "$feedback_block"
)

# Instruction logic
def level_instructions(level):
    return {
        5: "Keep the code very simple and easy to understand. Use basic constructs like loops, if statements, and simple functions.",
        4: "You may include file handling, lists, exception handling, or multiple functions.",
        3: "Include object-oriented programming, algorithmic logic, and reusable functions.",
        2: "Use advanced features like APIs, decorators, or concurrency if relevant.",
        1: "Incorporate cutting-edge techniques such as model inference, DSLs, or distributed logic.",
        0: "Explore unknown patterns and invent new solutions — treat this as a chance to create beyond current paradigms."
    }.get(level, "Write code appropriate to the goal.")

# Ask user how many generations to run
try:
    user_input = input("🎛️️ ️How many generations do you want to run? (0 = infinite): ")
    max_generations = int(user_input)
    if max_generations < 0:
        print("❌ Invalid input. Using default of 100 generations.")
        max_generations = 100
except ValueError:
    print("❌ Invalid input. Using default of 100 generations.")
    max_generations = 100

level = 5
generation = 1
past_feedback = ""

while True:
    print(f"\n🔍 Looking for prompts at level: {level}")
    try:
        prompt = get_prompt(level)
        print(f"📜 Prompt (Level {level}): {prompt}")
    except ValueError as e:
        print(f"❌ Error fetching prompt: {e}")
        break

    prompt_text = PROMPT_TEMPLATE.substitute(
        level=level,
        instructions=level_instructions(level),
        goal=prompt,
        feedback_block=(f"Past Feedback:\n{past_feedback}" if past_feedback else "")
    )

    print("\n🧪 Prompt for AI chamber execution:\n")
    print(prompt_text)

    try:
        generated_code = execute_code(prompt_text)
        print("\n📦 Generated Code:\n")
        print(generated_code)
    except Exception as e:
        print(f"❌ Code generation failed: {e}")
        generated_code = ""

    # ✅ Clean code
    cleaned_code = clean_code(generated_code)
    print("\n🔍 Cleaned Code to be Scored:\n", cleaned_code)

    # ✅ Score code
    try:
        scores = score_code(cleaned_code)

        # Normalize score if it's a single int
        if isinstance(scores, int):
            scores = {"execution": scores}

        print("\n📊 Score Summary:")
        for category, value in scores.items():
            print(f"- {category}: {value}")
    except Exception as e:
        print(f"❌ Scoring failed: {e}")
        scores = {}

    # ✅ Store only if execution score > 0
    if scores.get("execution", 0) > 0:
        store_snippet("python", code=cleaned_code, description=prompt, tags=["AI", "chamber", f"level-{level}"])
        print("💾 Snippet stored successfully.")
        log_event("store_snippet", f"gen_{generation}", language="python", details={"level": level, "scores": scores})
    else:
        print("⚠️ Skipping snippet storage due to low score.")

    # ✅ Log memory
    log_memory_entry({
        "generation": generation,
        "level": level,
        "prompt": prompt,
        "code": cleaned_code,
        "scores": scores,
        "feedback": past_feedback,
    })

    # Leveling logic
    if scores.get("execution", 0) >= 8 and scores.get("structure", 0) >= 8:
        level = max(level - 1, 0)
        print("📈 Leveling up! 🔼")
    elif scores.get("execution", 0) <= 3:
        level = min(level + 1, 5)
        print("📉 Leveling down! 🔽")

    generation += 1
    if max_generations != 0 and generation > max_generations:
        print("\n✅ Reached generation limit. Exiting loop.")
        break

