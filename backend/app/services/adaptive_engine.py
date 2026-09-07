from sqlalchemy.orm import Session

from app.models.attempt import QuizAttempt, QuizAnswer
from app.models.quiz import Question, Quiz
from app.models.lesson import Lesson


def analyze_performance(
    user_id: int,
    quiz_id: int,
    db: Session
):
    # Get latest attempt
    attempt = (
        db.query(QuizAttempt)
        .filter(
            QuizAttempt.user_id == user_id,
            QuizAttempt.quiz_id == quiz_id
        )
        .order_by(QuizAttempt.id.desc())
        .first()
    )

    if not attempt:
        return {
            "message": "No quiz attempt found"
        }

    # Get answers
    answers = (
        db.query(QuizAnswer)
        .filter(
            QuizAnswer.attempt_id == attempt.id
        )
        .all()
    )

    correct = sum(
        1 for answer in answers
        if answer.is_correct
    )

    total = len(answers)

    if total == 0:
        return {
            "message": "No answers found"
        }

    score = (correct / total) * 100

    # Determine learner level
    if score < 40:
        level = "beginner"
        recommendation_type = "revision"

    elif score < 70:
        level = "intermediate"
        recommendation_type = "practice"

    else:
        level = "advanced"
        recommendation_type = "progress"

    # Find current quiz
    quiz = (
        db.query(Quiz)
        .filter(Quiz.id == quiz_id)
        .first()
    )

    # Find current lesson
    current_lesson = None

    if quiz:
        current_lesson = (
            db.query(Lesson)
            .filter(
                Lesson.id == quiz.lesson_id
            )
            .first()
        )

    recommendation = None

    if current_lesson:

        if recommendation_type == "revision":
            recommendation = (
                f"Review the lesson '{current_lesson.title}' "
                f"and practice basic questions before moving ahead."
            )

        elif recommendation_type == "practice":
            recommendation = (
                f"Practice more questions related to "
                f"'{current_lesson.title}' before progressing."
            )

        else:
            recommendation = (
                f"You have demonstrated good understanding of "
                f"'{current_lesson.title}'. You can move to a "
                f"more advanced topic."
            )

    return {
        "user_id": user_id,
        "quiz_id": quiz_id,
        "attempt_id": attempt.id,
        "score": round(score, 2),
        "correct_answers": correct,
        "total_questions": total,
        "level": level,
        "recommendation_type": recommendation_type,
        "recommendation": recommendation
    }
def calculate_next_difficulty(score: float) -> str:
    """
    Determine the difficulty of the next learning activity
    based on the student's latest quiz score.
    """

    if score < 40:
        return "easy"

    elif score < 70:
        return "medium"

    else:
        return "hard"
def get_adaptive_questions(
    db,
    quiz_id: int,
    difficulty: str,
    limit: int = 5
):
    """
    Select questions matching the learner's current difficulty.
    """

    from app.models.quiz import Question

    questions = (
        db.query(Question)
        .filter(
            Question.quiz_id == quiz_id,
            Question.difficulty == difficulty
        )
        .limit(limit)
        .all()
    )

    return questions