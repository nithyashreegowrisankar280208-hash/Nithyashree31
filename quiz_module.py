import json
import re

from ai_client import generate_text


def generate_quiz(text: str) -> list:
    prompt = f"""
Create exactly 3 multiple-choice questions
based on the following study material.

Return ONLY a valid JSON array.

Each question must contain:
- question
- options: exactly 4 options
- answer: the exact correct option
- explanation: a short explanation

Example format:

[
  {{
    "question": "What is the largest ocean?",
    "options": [
      "Atlantic Ocean",
      "Indian Ocean",
      "Pacific Ocean",
      "Arctic Ocean"
    ],
    "answer": "Pacific Ocean",
    "explanation": "The Pacific Ocean is the largest ocean."
  }}
]

Create exactly 3 questions.

Study material:
{text}
"""

    response = generate_text(prompt)

    # Remove Markdown code fences if present.
    cleaned = re.sub(
        r"^\s*```(?:json)?\s*",
        "",
        response.strip(),
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"\s*```\s*$",
        "",
        cleaned
    )

    # Extract the JSON array.
    start = cleaned.find("[")
    end = cleaned.rfind("]")

    if start == -1 or end == -1:
        raise RuntimeError(
            "Could not find a valid quiz JSON array."
        )

    try:
        quiz = json.loads(cleaned[start:end + 1])
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Invalid quiz JSON: {error}"
        ) from error

    if not isinstance(quiz, list) or len(quiz) != 3:
        raise RuntimeError(
            "The quiz must contain exactly 3 questions."
        )

    for question in quiz:
        if not isinstance(question, dict):
            raise RuntimeError("Invalid question format.")

        if len(question.get("options", [])) != 4:
            raise RuntimeError(
                "Each question must have 4 options."
            )

        if question.get("answer") not in question["options"]:
            raise RuntimeError(
                "The correct answer must match an option."
            )

        for field in (
            "question",
            "answer",
            "explanation"
        ):
            if not question.get(field):
                raise RuntimeError(
                    f"Missing quiz field: {field}"
                )

    return quiz