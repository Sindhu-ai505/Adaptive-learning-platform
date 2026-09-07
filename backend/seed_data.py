"""
Full database seed script.
Creates 3 courses → lessons → quizzes → questions (easy/medium/hard).
Safe to re-run: skips anything that already exists.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

# Load .env from project root if present
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass

os.environ.setdefault("DATABASE_URL", "sqlite:///./adaptive_learning.db")
os.environ.setdefault("SECRET_KEY", "seed-script-secret")

from app.core.database import SessionLocal, Base, engine
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.quiz import Quiz, Question

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ─────────────────────────────────────────────────────────────────────────────
# DATA DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

COURSES = [
    {
        "title": "Introduction to Artificial Intelligence",
        "description": "A beginner-friendly introduction to AI concepts, history, and applications in the real world.",
        "difficulty": "beginner",
        "category": "AI",
        "lessons": [
            {
                "title": "What is Artificial Intelligence?",
                "content": (
                    "Artificial Intelligence (AI) is the simulation of human intelligence in machines programmed to think, "
                    "learn, and solve problems. AI encompasses a range of technologies including machine learning, natural "
                    "language processing, computer vision, and robotics.\n\n"
                    "Key branches of AI:\n"
                    "• Machine Learning – systems that learn from data\n"
                    "• Natural Language Processing – understanding human language\n"
                    "• Computer Vision – interpreting images and video\n"
                    "• Expert Systems – rule-based decision making\n\n"
                    "AI is used in search engines, recommendation systems, autonomous vehicles, medical diagnosis, and much more."
                ),
                "difficulty": "beginner",
                "order": 1,
                "quiz_title": "AI Fundamentals Quiz",
                "questions": [
                    # EASY
                    {
                        "text": "What does AI stand for?",
                        "a": "Artificial Intelligence", "b": "Automated Input",
                        "c": "Advanced Integration", "d": "Automated Intelligence",
                        "ans": "A", "difficulty": "easy",
                    },
                    {
                        "text": "Which of the following is an example of AI in everyday life?",
                        "a": "A light switch", "b": "A voice assistant like Siri",
                        "c": "A paper book", "d": "A wooden chair",
                        "ans": "B", "difficulty": "easy",
                    },
                    {
                        "text": "Which programming language is most commonly used in AI development?",
                        "a": "HTML", "b": "CSS", "c": "Python", "d": "Excel",
                        "ans": "C", "difficulty": "easy",
                    },
                    # MEDIUM
                    {
                        "text": "What is the branch of AI that enables computers to learn from data?",
                        "a": "Expert Systems", "b": "Machine Learning",
                        "c": "Database Management", "d": "Compiler Design",
                        "ans": "B", "difficulty": "medium",
                    },
                    {
                        "text": "Which AI subfield focuses on understanding and generating human language?",
                        "a": "Computer Vision", "b": "Robotics",
                        "c": "Natural Language Processing", "d": "Cloud Computing",
                        "ans": "C", "difficulty": "medium",
                    },
                    {
                        "text": "What is a neural network loosely modelled on?",
                        "a": "Spreadsheets", "b": "The human brain",
                        "c": "Database tables", "d": "File systems",
                        "ans": "B", "difficulty": "medium",
                    },
                    # HARD
                    {
                        "text": "Which type of learning uses rewards and penalties to train an agent?",
                        "a": "Supervised learning", "b": "Unsupervised learning",
                        "c": "Reinforcement learning", "d": "Transfer learning",
                        "ans": "C", "difficulty": "hard",
                    },
                    {
                        "text": "What does the Turing Test evaluate?",
                        "a": "Processing speed of a computer",
                        "b": "Whether a machine can exhibit intelligent behaviour indistinguishable from a human",
                        "c": "Memory capacity of an AI model",
                        "d": "The accuracy of a recommendation engine",
                        "ans": "B", "difficulty": "hard",
                    },
                    {
                        "text": "In machine learning, what is overfitting?",
                        "a": "When a model performs poorly on training data",
                        "b": "When a model memorises training data and fails to generalise",
                        "c": "When a model trains too slowly",
                        "d": "When the dataset is too small to use",
                        "ans": "B", "difficulty": "hard",
                    },
                ],
            },
            {
                "title": "History and Evolution of AI",
                "content": (
                    "AI has a rich history dating back to the 1950s.\n\n"
                    "Timeline:\n"
                    "• 1950 – Alan Turing proposes the Turing Test\n"
                    "• 1956 – The term 'Artificial Intelligence' coined at Dartmouth\n"
                    "• 1966 – ELIZA chatbot created at MIT\n"
                    "• 1997 – IBM Deep Blue defeats chess champion Garry Kasparov\n"
                    "• 2012 – Deep learning breakthrough with AlexNet\n"
                    "• 2016 – AlphaGo defeats world Go champion\n"
                    "• 2022 – ChatGPT reaches 100 million users in 2 months\n\n"
                    "AI research went through periods of excitement ('AI summers') and funding cuts ('AI winters')."
                ),
                "difficulty": "beginner",
                "order": 2,
                "quiz_title": "AI History Quiz",
                "questions": [
                    {
                        "text": "Who proposed the Turing Test in 1950?",
                        "a": "Alan Turing", "b": "John McCarthy",
                        "c": "Marvin Minsky", "d": "Geoffrey Hinton",
                        "ans": "A", "difficulty": "easy",
                    },
                    {
                        "text": "In which year was the term 'Artificial Intelligence' coined?",
                        "a": "1940", "b": "1956", "c": "1970", "d": "1985",
                        "ans": "B", "difficulty": "easy",
                    },
                    {
                        "text": "What was Deep Blue?",
                        "a": "An early internet browser",
                        "b": "IBM's chess-playing computer that defeated Kasparov",
                        "c": "A natural language processing model",
                        "d": "An AI-powered search engine",
                        "ans": "B", "difficulty": "medium",
                    },
                    {
                        "text": "What is an 'AI winter'?",
                        "a": "A period of rapid AI advancement",
                        "b": "A period of reduced AI funding and interest",
                        "c": "A seasonal AI conference",
                        "d": "A cold-start problem in machine learning",
                        "ans": "B", "difficulty": "medium",
                    },
                    {
                        "text": "Which breakthrough in 2012 significantly advanced deep learning?",
                        "a": "GPT-3", "b": "AlphaGo", "c": "AlexNet", "d": "BERT",
                        "ans": "C", "difficulty": "hard",
                    },
                    {
                        "text": "What game did AlphaGo master, defeating the world champion in 2016?",
                        "a": "Chess", "b": "Checkers", "c": "Poker", "d": "Go",
                        "ans": "D", "difficulty": "hard",
                    },
                ],
            },
        ],
    },
    {
        "title": "Machine Learning Fundamentals",
        "description": "Learn core ML concepts: supervised, unsupervised, and reinforcement learning with hands-on examples.",
        "difficulty": "intermediate",
        "category": "Machine Learning",
        "lessons": [
            {
                "title": "Supervised Learning",
                "content": (
                    "Supervised learning is the most common type of machine learning. The algorithm learns from labelled "
                    "training data — each example has an input and a known correct output.\n\n"
                    "Common algorithms:\n"
                    "• Linear Regression – predicts continuous values (e.g. house prices)\n"
                    "• Logistic Regression – binary classification (e.g. spam/not spam)\n"
                    "• Decision Trees – tree-like model of decisions\n"
                    "• Random Forest – ensemble of decision trees\n"
                    "• Support Vector Machines (SVM) – finds the optimal boundary between classes\n"
                    "• Neural Networks – learns complex non-linear patterns\n\n"
                    "Key concepts: training set, validation set, test set, loss function, gradient descent."
                ),
                "difficulty": "intermediate",
                "order": 1,
                "quiz_title": "Supervised Learning Quiz",
                "questions": [
                    {
                        "text": "In supervised learning, the training data is:",
                        "a": "Unlabelled", "b": "Labelled with correct outputs",
                        "c": "Generated randomly", "d": "Always numerical",
                        "ans": "B", "difficulty": "easy",
                    },
                    {
                        "text": "Which algorithm is best suited for predicting a continuous numeric value?",
                        "a": "Logistic Regression", "b": "K-Means",
                        "c": "Linear Regression", "d": "DBSCAN",
                        "ans": "C", "difficulty": "easy",
                    },
                    {
                        "text": "What is the purpose of a loss function?",
                        "a": "To generate new training data",
                        "b": "To measure how far the model's predictions are from the true values",
                        "c": "To split data into train and test sets",
                        "d": "To visualise the model architecture",
                        "ans": "B", "difficulty": "medium",
                    },
                    {
                        "text": "A Random Forest is best described as:",
                        "a": "A single large decision tree",
                        "b": "An ensemble of multiple decision trees",
                        "c": "A type of neural network",
                        "d": "A clustering algorithm",
                        "ans": "B", "difficulty": "medium",
                    },
                    {
                        "text": "What is gradient descent used for?",
                        "a": "Normalising input data",
                        "b": "Minimising the loss function by iteratively updating model parameters",
                        "c": "Splitting data into batches",
                        "d": "Removing outliers from the dataset",
                        "ans": "B", "difficulty": "medium",
                    },
                    {
                        "text": "Which of the following is a sign of overfitting?",
                        "a": "High training accuracy, low test accuracy",
                        "b": "Low training accuracy, high test accuracy",
                        "c": "Equal training and test accuracy",
                        "d": "The model converges very quickly",
                        "ans": "A", "difficulty": "hard",
                    },
                    {
                        "text": "What does regularisation (L1/L2) do in a machine learning model?",
                        "a": "Speeds up training", "b": "Adds a penalty to large weights to prevent overfitting",
                        "c": "Increases the learning rate", "d": "Removes features from the dataset",
                        "ans": "B", "difficulty": "hard",
                    },
                    {
                        "text": "What is cross-validation used for?",
                        "a": "To increase the size of the dataset",
                        "b": "To estimate how well a model generalises to unseen data",
                        "c": "To visualise model predictions",
                        "d": "To apply PCA to the dataset",
                        "ans": "B", "difficulty": "hard",
                    },
                ],
            },
            {
                "title": "Unsupervised Learning",
                "content": (
                    "Unsupervised learning finds hidden patterns in data without labelled examples.\n\n"
                    "Main types:\n"
                    "• Clustering – grouping similar data points\n"
                    "  - K-Means: assigns points to K clusters by minimising distance to centroids\n"
                    "  - DBSCAN: density-based clustering, handles noise\n"
                    "  - Hierarchical: builds a tree of clusters\n\n"
                    "• Dimensionality Reduction – compressing data while retaining key information\n"
                    "  - PCA (Principal Component Analysis): finds directions of maximum variance\n"
                    "  - t-SNE: visualises high-dimensional data in 2D/3D\n\n"
                    "• Anomaly Detection – identifying unusual data points\n\n"
                    "Applications: customer segmentation, topic modelling, fraud detection, image compression."
                ),
                "difficulty": "intermediate",
                "order": 2,
                "quiz_title": "Unsupervised Learning Quiz",
                "questions": [
                    {
                        "text": "Unsupervised learning differs from supervised learning because:",
                        "a": "It uses labelled training data",
                        "b": "It works with unlabelled data and finds hidden patterns",
                        "c": "It always requires a neural network",
                        "d": "It can only be used for classification",
                        "ans": "B", "difficulty": "easy",
                    },
                    {
                        "text": "Which algorithm groups data into K clusters by minimising distance to centroids?",
                        "a": "Linear Regression", "b": "SVM", "c": "K-Means", "d": "Random Forest",
                        "ans": "C", "difficulty": "easy",
                    },
                    {
                        "text": "What does PCA stand for?",
                        "a": "Principal Component Analysis", "b": "Partial Cluster Algorithm",
                        "c": "Predictive Classification Approach", "d": "Processed Conditional Analysis",
                        "ans": "A", "difficulty": "medium",
                    },
                    {
                        "text": "What is the main goal of dimensionality reduction?",
                        "a": "To add more features to the dataset",
                        "b": "To reduce the number of features while preserving important information",
                        "c": "To split the dataset into training and test sets",
                        "d": "To apply labels to unlabelled data",
                        "ans": "B", "difficulty": "medium",
                    },
                    {
                        "text": "DBSCAN is best suited for:",
                        "a": "Linear classification problems",
                        "b": "Clustering data with arbitrary shapes and noise",
                        "c": "Predicting house prices",
                        "d": "Reducing dimensionality",
                        "ans": "B", "difficulty": "hard",
                    },
                    {
                        "text": "t-SNE is primarily used for:",
                        "a": "Training deep neural networks",
                        "b": "Visualising high-dimensional data in 2D or 3D",
                        "c": "Performing binary classification",
                        "d": "Speeding up gradient descent",
                        "ans": "B", "difficulty": "hard",
                    },
                ],
            },
        ],
    },
    {
        "title": "Deep Learning & Neural Networks",
        "description": "Dive into deep learning: neural network architectures, CNNs, RNNs, Transformers and real-world applications.",
        "difficulty": "advanced",
        "category": "Deep Learning",
        "lessons": [
            {
                "title": "Neural Network Basics",
                "content": (
                    "A neural network is a computational model inspired by the structure of the human brain.\n\n"
                    "Key components:\n"
                    "• Neurons (nodes) – basic computational units\n"
                    "• Layers: Input layer → Hidden layers → Output layer\n"
                    "• Weights & Biases – learnable parameters\n"
                    "• Activation Functions – introduce non-linearity (ReLU, Sigmoid, Tanh, Softmax)\n"
                    "• Forward Pass – computing predictions from input to output\n"
                    "• Backpropagation – computing gradients to update weights\n\n"
                    "Training loop:\n"
                    "1. Forward pass → compute loss\n"
                    "2. Backpropagation → compute gradients\n"
                    "3. Gradient descent → update weights\n"
                    "4. Repeat for many epochs"
                ),
                "difficulty": "advanced",
                "order": 1,
                "quiz_title": "Neural Networks Quiz",
                "questions": [
                    {
                        "text": "What are the learnable parameters in a neural network called?",
                        "a": "Layers and nodes", "b": "Weights and biases",
                        "c": "Inputs and outputs", "d": "Epochs and batches",
                        "ans": "B", "difficulty": "easy",
                    },
                    {
                        "text": "Which activation function outputs values between 0 and 1?",
                        "a": "ReLU", "b": "Tanh", "c": "Sigmoid", "d": "Softmax",
                        "ans": "C", "difficulty": "easy",
                    },
                    {
                        "text": "What is the purpose of backpropagation?",
                        "a": "To generate training data",
                        "b": "To compute gradients of the loss with respect to model weights",
                        "c": "To normalise input features",
                        "d": "To select hyperparameters",
                        "ans": "B", "difficulty": "medium",
                    },
                    {
                        "text": "ReLU activation function outputs:",
                        "a": "Values between -1 and 1",
                        "b": "Values between 0 and 1",
                        "c": "Max(0, x) — zero for negatives, x for positives",
                        "d": "Always exactly 0 or 1",
                        "ans": "C", "difficulty": "medium",
                    },
                    {
                        "text": "What is the vanishing gradient problem?",
                        "a": "When the model weights become too large",
                        "b": "When gradients become very small in deep networks, slowing or stopping learning",
                        "c": "When the dataset is too small for training",
                        "d": "When the learning rate is set too high",
                        "ans": "B", "difficulty": "hard",
                    },
                    {
                        "text": "Dropout in neural networks is used to:",
                        "a": "Speed up inference", "b": "Reduce the number of layers",
                        "c": "Prevent overfitting by randomly deactivating neurons during training",
                        "d": "Increase the learning rate",
                        "ans": "C", "difficulty": "hard",
                    },
                    {
                        "text": "Batch normalisation helps by:",
                        "a": "Reducing the number of training examples needed",
                        "b": "Normalising layer inputs to speed up training and stabilise learning",
                        "c": "Converting labels to one-hot encoding",
                        "d": "Increasing model depth",
                        "ans": "B", "difficulty": "hard",
                    },
                ],
            },
            {
                "title": "Transformers & Large Language Models",
                "content": (
                    "The Transformer architecture (introduced in 'Attention Is All You Need', 2017) revolutionised AI.\n\n"
                    "Core concepts:\n"
                    "• Self-Attention – each token attends to all other tokens in the sequence\n"
                    "• Multi-Head Attention – multiple attention heads capture different relationships\n"
                    "• Positional Encoding – adds sequence order information\n"
                    "• Encoder-Decoder – encoder reads input, decoder generates output\n\n"
                    "Famous Transformer-based models:\n"
                    "• BERT (Google, 2018) – bidirectional encoder for understanding tasks\n"
                    "• GPT series (OpenAI) – autoregressive decoder for text generation\n"
                    "• T5, LLaMA, Mistral, Claude, Gemini\n\n"
                    "LLMs are pre-trained on massive text corpora and fine-tuned for specific tasks."
                ),
                "difficulty": "advanced",
                "order": 2,
                "quiz_title": "Transformers Quiz",
                "questions": [
                    {
                        "text": "What is the key mechanism in the Transformer architecture?",
                        "a": "Convolution", "b": "Recurrence", "c": "Self-Attention", "d": "Pooling",
                        "ans": "C", "difficulty": "easy",
                    },
                    {
                        "text": "What does BERT stand for?",
                        "a": "Bidirectional Encoder Representations from Transformers",
                        "b": "Basic Encoder with Recurrent Transformers",
                        "c": "Binary Encoded Recurrent Text",
                        "d": "Batch Encoding and Retrieval Tool",
                        "ans": "A", "difficulty": "easy",
                    },
                    {
                        "text": "Positional encoding in Transformers is used to:",
                        "a": "Reduce the model size",
                        "b": "Inject information about the order of tokens in the sequence",
                        "c": "Apply dropout to attention weights",
                        "d": "Normalise the attention scores",
                        "ans": "B", "difficulty": "medium",
                    },
                    {
                        "text": "Multi-head attention allows the model to:",
                        "a": "Process multiple input sequences simultaneously",
                        "b": "Attend to different representation subspaces at different positions",
                        "c": "Skip certain layers during training",
                        "d": "Reduce memory usage",
                        "ans": "B", "difficulty": "medium",
                    },
                    {
                        "text": "GPT models are primarily based on which part of the Transformer?",
                        "a": "Encoder only", "b": "Decoder only",
                        "c": "Encoder-Decoder", "d": "Convolutional layers",
                        "ans": "B", "difficulty": "hard",
                    },
                    {
                        "text": "What is fine-tuning in the context of LLMs?",
                        "a": "Training a model from scratch on a new dataset",
                        "b": "Further training a pre-trained model on a specific task with a smaller dataset",
                        "c": "Compressing a model to reduce its size",
                        "d": "Increasing the number of attention heads",
                        "ans": "B", "difficulty": "hard",
                    },
                ],
            },
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# SEEDING LOGIC
# ─────────────────────────────────────────────────────────────────────────────

def seed():
    total_courses = 0
    total_lessons = 0
    total_quizzes = 0
    total_questions = 0

    for c_data in COURSES:
        # Check if course already exists
        existing = db.query(Course).filter(Course.title == c_data["title"]).first()
        if existing:
            print(f"  [skip] Course already exists: '{c_data['title']}'")
            continue

        course = Course(
            title=c_data["title"],
            description=c_data["description"],
            difficulty=c_data["difficulty"],
            category=c_data["category"],
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        total_courses += 1
        print(f"  [+] Course: '{course.title}' (id={course.id})")

        for l_data in c_data["lessons"]:
            lesson = Lesson(
                course_id=course.id,
                title=l_data["title"],
                content=l_data["content"],
                difficulty=l_data["difficulty"],
                order=l_data["order"],
            )
            db.add(lesson)
            db.commit()
            db.refresh(lesson)
            total_lessons += 1
            print(f"       [+] Lesson: '{lesson.title}' (id={lesson.id})")

            quiz = Quiz(
                lesson_id=lesson.id,
                title=l_data["quiz_title"],
            )
            db.add(quiz)
            db.commit()
            db.refresh(quiz)
            total_quizzes += 1
            print(f"            [+] Quiz: '{quiz.title}' (id={quiz.id})")

            for q in l_data["questions"]:
                question = Question(
                    quiz_id=quiz.id,
                    question_text=q["text"],
                    option_a=q["a"],
                    option_b=q["b"],
                    option_c=q["c"],
                    option_d=q["d"],
                    correct_answer=q["ans"],
                    difficulty=q["difficulty"],
                )
                db.add(question)
                total_questions += 1

            db.commit()
            print(f"                 [+] {len(l_data['questions'])} questions added")

    db.close()
    print()
    print("=" * 50)
    print(f"Seeding complete!")
    print(f"  Courses:   {total_courses}")
    print(f"  Lessons:   {total_lessons}")
    print(f"  Quizzes:   {total_quizzes}")
    print(f"  Questions: {total_questions}")
    print("=" * 50)

    if total_courses == 0:
        print("(Nothing new was added — data already existed)")


if __name__ == "__main__":
    print("Seeding database...")
    seed()
