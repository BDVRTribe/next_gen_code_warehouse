import ast

def generate_code(goal, dry_run=True):
    from phase_4.gpt_llm import gpt_llm

    goal_text = goal.get("goal_text", "")
    prompt = (
        f"You are a Python coding assistant.\n"
        f"Write only Python code to implement the following goal:\n\n"
        f"{goal_text}\n\n"
        f"Respond with valid, executable Python code only. No explanations, no markdown, no comments."
    )
    code = gpt_llm(prompt).strip()

    # 🔧 Clean the code of Markdown formatting
    if code.startswith("```"):
        code = code.strip("`")  # Remove all backticks
        if code.lower().startswith("python"):
            code = code[6:].strip()

    # Optional preview
    if dry_run:
        print("\n🧾 Suggested Code:\n")
        print(code)
        confirm = input("\n💡 Proceed with execution? (Y/n): ").strip().lower()
        if confirm not in ("y", "yes", ""):
            print("⛔ Skipping execution.")
            return {"code": code, "valid": False, "reason": "User skipped execution."}

    # AST validation
    try:
        ast.parse(code)
        return {"code": code, "valid": True, "reason": None}
    except SyntaxError as e:
        print("❌ Syntax error in generated code. Skipping execution.")
        return {"code": code, "valid": False, "reason": str(e)}

