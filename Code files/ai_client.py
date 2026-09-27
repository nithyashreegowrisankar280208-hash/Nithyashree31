import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai

load_dotenv()


@lru_cache(maxsize=1)
def get_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key or api_key == "your_actual_api_key":
        raise RuntimeError(
            "Gemini API key is missing. Add it to your .env file."
        )

    return genai.Client(api_key=api_key)


def generate_text(prompt: str) -> str:
    client = get_client()

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    answer = response.text

    if not answer:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return answer.strip()