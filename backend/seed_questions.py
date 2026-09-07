from app.core.database import SessionLocal
from app.models.quiz import Question


db = SessionLocal()

questions = [
    # EASY
    Question(
        quiz_id=1,
        question_text="What is 2 + 2?",
        option_a="3",
        option_b="4",
        option_c="5",
        option_d="6",
        correct_answer="B",
        difficulty="easy",
    ),
    Question(
        quiz_id=1,
        question_text="Which language is commonly used for AI?",
        option_a="Python",
        option_b="HTML",
        option_c="CSS",
        option_d="XML",
        correct_answer="A",
        difficulty="easy",
    ),

    # MEDIUM
    Question(
        quiz_id=1,
        question_text="What does NLP stand for?",
        option_a="Natural Language Processing",
        option_b="Neural Learning Program",
        option_c="Natural Logic Programming",
        option_d="Network Language Protocol",
        correct_answer="A",
        difficulty="medium",
    ),
    Question(
        quiz_id=1,
        question_text="Which algorithm is commonly used for classification?",
        option_a="Linear Regression",
        option_b="Decision Tree",
        option_c="PCA",
        option_d="K-Means",
        correct_answer="B",
        difficulty="medium",
    ),

    # HARD
    Question(
        quiz_id=1,
        question_text="Which technique is commonly used to reduce dimensionality?",
        option_a="PCA",
        option_b="Bagging",
        option_c="Gradient Descent",
        option_d="Tokenization",
        correct_answer="A",
        difficulty="hard",
    ),
    Question(
        quiz_id=1,
        question_text="What is the primary purpose of attention in Transformers?",
        option_a="Database storage",
        option_b="Focus on relevant input tokens",
        option_c="Image compression",
        option_d="File encryption",
        correct_answer="B",
        difficulty="hard",
    ),
]


try:
    db.add_all(questions)
    db.commit()
    print("Questions inserted successfully!")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()