"""
LLM feedback service.
Uses transformers/distilgpt2 locally when available.
Falls back to rule-based feedback for cloud deployment
where the heavy torch/transformers packages are not installed.
"""

def generate_feedback(score: float, level: str, recommendation: str) -> str:
    # Try the real LLM first (works locally with torch installed)
    try:
        from transformers import pipeline  # noqa: PLC0415

        _gen = pipeline("text-generation", model="distilgpt2")
        prompt = (
            f"You are an AI tutor.\n"
            f"Student quiz score: {score} percent.\n"
            f"Student level: {level}.\n"
            f"Recommended action: {recommendation}.\n"
            f"Give short personalized feedback."
        )
        result = _gen(prompt, max_new_tokens=80, do_sample=True, temperature=0.7)
        return result[0]["generated_text"]

    except Exception:
        pass

    # Rule-based fallback (no dependencies needed)
    return _rule_based_feedback(score, level, recommendation)


def _rule_based_feedback(score: float, level: str, recommendation: str) -> str:
    if score >= 70:
        opening = f"Excellent work! You scored {score:.0f}% — that is a strong result."
        improvement = "Continue challenging yourself with more advanced material."
    elif score >= 40:
        opening = f"Good effort! You scored {score:.0f}% and are making solid progress."
        improvement = "Review the topics where you made mistakes and practise similar questions."
    else:
        opening = f"You scored {score:.0f}%. Do not be discouraged — every expert started as a beginner."
        improvement = "Go back and re-read the lesson carefully before attempting the quiz again."

    return (
        f"{opening} "
        f"Your current learning level is {level}. "
        f"{improvement} "
        f"Next step: {recommendation}"
    )