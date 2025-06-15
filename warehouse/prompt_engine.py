import json
import random

def get_prompt(level):
    with open("phase_4/prompt_bank.json", "r") as f:
        all_prompts = json.load(f)

    level_str = str(level)
    print(f"🔍 Looking for prompts at level: {level_str}")
    print(f"📚 Available levels: {list(all_prompts.keys())}")

    try:
        prompts = all_prompts[level_str]
        if not prompts:
            raise ValueError
    except (KeyError, ValueError):
        raise ValueError(f"⚠️ No prompts found or prompt list is empty for level {level_str}")

    # If prompts is a dict (e.g., {"0": "...", "1": "..."}) → convert to list
    if isinstance(prompts, dict):
        prompts = list(prompts.values())

    if not isinstance(prompts, list) or len(prompts) == 0:
        raise ValueError(f"❌ Prompt format error: Expected a non-empty list, got {type(prompts)}")

    prompt_data = random.choice(prompts)

    # Support various prompt formats
    if isinstance(prompt_data, str):
        return prompt_data
    elif isinstance(prompt_data, list):
        return "\n".join([item['content'] for item in prompt_data if 'content' in item])
    elif isinstance(prompt_data, dict):
        return prompt_data.get('content', json.dumps(prompt_data))
    else:
        raise ValueError(f"❌ Unsupported prompt format: {prompt_data}")

