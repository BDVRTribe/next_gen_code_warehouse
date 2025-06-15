import json
import uuid
import random
from string import Template
from openai import OpenAI
from warehouse.core import store_snippet
from warehouse.executor import execute_code
from warehouse.logger import log_event

# ✅ Load OpenAI API key
with open("phase_4/openai_key.txt") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

# ✅ Instructions per level
def level_instructions(level):
    return {
        5: "Keep the code very simple and easy to understand. Use basic constructs like loops, if statements, and simple functions.",
        4: "You may include file handling, lists, exception handling, or multiple functions.",
        3: "Include object-oriented programming, algorithmic logic, and reusable functions.",
        2: "Use advanced features like APIs, decorators, or concurrency if relevant.",
        1: "Incorporate cutting-edge techniques such as model inference, DSLs, or distributed logic.",
        0: "Explore unknown patterns and invent new solutions — treat this as a chance to create beyond current paradigms."
    }.get(level, "Write code appropriate to the goal.")

# ✅ Prompt Template
PROMPT_TEMPLATE = Template(
    "You are an expert Python programmer."
    "\nTask Level: $level (5=beginner, 0=revolutionary)\n\n"
    "Instructions:\n$instructions\n\n"
    "Goal:\n$goal\n\n"
    "$feedback_block"
)

# ✅ Load prompt bank
with open("phase_4/prompt_bank.json") as f:
    prompt_bank = json.load(f)

# ✅ Run Chamber
def run_chamber(goal=None):
    current_level = 5
    memory_log = []
    generation = 1

    try:
        while True:
            print(f"\n🔁 Generation {generation} at Level {current_level}\n")

            # 🔄 Select prompt
            if goal:
                goal_text = goal["goal_text"]
            else:
                goal_text = random.choice(prompt_bank)

            # 🧠 Feedback block
            feedback_block = ""
            if memory_log:
                feedback_block = "Past Feedback:\n" + "\n".join(memory_log[-3:]) + "\n\n"

            prompt = PROMPT_TEMPLATE.substitute(
                level=current_level,
                instructions=level_instructions(current_level),
                goal=goal_text,
                feedback_block=feedback_block
            )

            # 🔮 Generate code from GPT
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            code = response.choices[0].message.content.strip()

            print(f"\n🧾 Suggested Code:\n {code}\n")
            proceed = input("💡 Proceed with execution? (Y/n): ").strip().lower()

            if proceed == "n":
                print("\n👋 Session ended by user.")
                break

            # 🧪 Execute code
            success = execute_code(code)
            score = 100 if success else random.randint(20, 60)
            memory_log.append(f"Gen {generation}: Score {score}")

            # 🧬 Level adjust
            if score >= 95:
                current_level = max(current_level - 1, 0)
            else:
                current_level = min(current_level + 1, 5)

            # 💾 Store
            snippet_data = {
                "title": f"gen_{generation}_level_{current_level}_{uuid.uuid4().hex[:4]}",
                "code": code,
                "description": goal_text,
                "tags": ["AI", "chamber", f"level-{current_level}"]
            }

            store_snippet("python", **snippet_data)
            generation += 1

    except KeyboardInterrupt:
        print("\n👋 Session interrupted by user (Ctrl+C). Exiting.")

