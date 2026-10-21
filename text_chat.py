import os

from dotenv import load_dotenv
from openai import OpenAI

from ai_agent import SYSTEM_PROMPT

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not api_key:
    raise ValueError("OpenAI API key is missing. Check your .env file.")

client = OpenAI(api_key=api_key)


def get_ai_response(messages):

    response = client.responses.create(
        model=model,
        instructions=SYSTEM_PROMPT,
        input=messages
    )

    return response.output_text