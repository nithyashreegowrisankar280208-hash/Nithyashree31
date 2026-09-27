from ai_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question accurately.
Use simple English that students can understand.

Give:
1. A direct answer
2. A short explanation
3. An example if necessary

Student's question:
{question}
"""

    return generate_text(prompt)