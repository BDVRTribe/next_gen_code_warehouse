# phase_4/gpt_llm.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client using API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Main LLM function to return a unique AI experiment description
def gpt_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",  # GPT-4.1 Mini
        messages=[
            {
                "role": "system",
                "content": "You are an expert AI researcher tasked with generating diverse, innovative, and practical AI experiments across various domains like robotics, science, sustainability, healthcare, education, and creative media."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.9,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

