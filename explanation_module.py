from ai_client import generate_text


def explain_topic(topic: str) -> str:
    prompt = f"""
You are EduGenie, a friendly teacher.

Explain the following topic to a beginner.

Use:
1. Definition
2. Simple explanation
3. Step-by-step points
4. One easy example
5. Short conclusion

Use simple English.
Avoid difficult technical words.

Topic:
{topic}
"""

    return generate_text(prompt)