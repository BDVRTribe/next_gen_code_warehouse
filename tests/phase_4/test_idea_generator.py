import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from phase_4.idea_generator import generate_idea, save_idea

def mock_llm(prompt):
    return "Title: AI-powered Mutation Refinement\nDescription: Use a language model to iteratively mutate Python code based on sandbox feedback.\nTags: ['ai', 'mutation', 'llm', 'code evolution']"

def test_generate_and_save_idea():
    idea = generate_idea(mock_llm)
    assert "description" in idea
    assert "created_at" in idea
    save_idea(idea, archive_path="tests/phase_4/test_idea_archive.json")


