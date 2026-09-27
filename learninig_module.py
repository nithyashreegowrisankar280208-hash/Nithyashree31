from ai_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
You are EduGenie, a personal learning guide.

Create a learning roadmap for:
{topic}

Organize the roadmap into:

1. Beginner Level
2. Intermediate Level
3. Advanced Level

For each level, include:
- Topics to study
- Suggested learning timeline
- Practice activities
- A small project

Also include:
- Recommended types of learning resources
- A final project
- Tips for consistent learning

Use simple English.
Make the roadmap practical for a student.
"""

    return generate_text(prompt)