from transformers import pipeline


_generator = None


def get_generator():
    global _generator

    if _generator is None:
        _generator = pipeline(
            "text-generation",
            model="distilgpt2"
        )

    return _generator


def generate_feedback(
    score: float,
    level: str,
    recommendation: str
):
    generator = get_generator()

    prompt = f"""
You are an AI tutor.

Student quiz score: {score} percent.
Student level: {level}.
Recommended action: {recommendation}.

Give short personalized feedback.
Mention what the student did well,
what they should improve,
and what they should study next.
"""

    result = generator(
        prompt,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.7
    )

    return result[0]["generated_text"]