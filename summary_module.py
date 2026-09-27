from ai_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
You are EduGenie, an educational assistant.

Summarize the following passage for a student.

Requirements:
- Use simple English.
- Keep the important facts.
- Remove unnecessary repetition.
- Use bullet points where helpful.
- Do not add unsupported information.

Passage:
{text}
"""

    return generate_text(prompt)