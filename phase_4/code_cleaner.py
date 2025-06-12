import re

def clean_code(code_str):
    """Extracts the first valid Python code block from a GPT response. Removes markdown fences and explanations."""
    match = re.search(r"```(?:python)?\n([\s\S]*?)```", code_str)
    if match:
        return match.group(1).strip()
    else:
        # Remove common markdown and explanation prefixes
        lines = code_str.strip().splitlines()
        code_lines = [
            line for line in lines
            if not line.lower().startswith((
                "sure!", "here", "this", "you can", "example", "---"
            ))
        ]
        return "\n".join(code_lines).strip()

