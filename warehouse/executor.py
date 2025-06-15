import traceback
import re
import sys
import os
from openai import OpenAI

from warehouse.prompt_engine import get_prompt
from warehouse.logger import log_event, log_undo_action
from warehouse.core import store_snippet

# ✅ Load the OpenAI API key from the unified key file
api_key_path = "phase_4/openai_key.txt"
with open(api_key_path) as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

def clean_code(code_str):
    """Extracts the first valid Python code block from a GPT response. Removes markdown fences and explanations."""
    match = re.search(r"```(?:python)?\n([\s\S]*?)```", code_str)
    if match:
        return match.group(1).strip()
    else:
        lines = code_str.strip().splitlines()
        code_lines = [
            line for line in lines
            if not line.lower().startswith(("sure!", "here", "this", "you can", "example", "---"))
        ]
        return "\n".join(code_lines).strip()

def execute_code(prompt):
    """
    Calls GPT-4.1-mini with the provided prompt and returns the generated code string.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an expert Python programmer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Error during GPT API call: {e}")
        return None

def chamber_loop():
    try:
        max_generations = input("🔧 How many generations do you want to run? (default 100): ").strip()
        max_generations = int(max_generations) if max_generations.isdigit() else 100
    except:
        max_generations = 100

    current_level = 5
    gen_number = 1

    try:
        while gen_number <= max_generations:
            print(f"\n🔁 Generation {gen_number} at Level {current_level}")
            prompt = get_prompt(current_level)
            print("\n📜 Prompt:\n", prompt)

            raw_code = execute_code(prompt)
            if raw_code is None:
                print("⚠️ Code generation failed. Skipping to next.")
                gen_number += 1
                continue

            code = clean_code(raw_code)
            print("\n💡 Generated Code:\n")
            print(code)

            # Optional: execute the code (if safe — this is sandbox-sensitive)
            # exec(code, globals())

            # Log or store the snippet
            store_snippet("python", code=code, description=prompt, tags=["generated"])
            log_event("generate", f"gen_{gen_number}", language="python", details={"level": current_level})

            gen_number += 1

    except KeyboardInterrupt:
        print("\n🚪 Interrupted by user. Exiting chamber loop.")

