"""
Extended AIML curriculum seed — 9 new courses.
Safe to re-run: skips courses whose title already exists.

Curriculum map
──────────────
BEGINNER
  4. Python for AI & Data Science
  5. Mathematics for Machine Learning
  6. Data Analysis & Visualisation

INTERMEDIATE
  7. Computer Vision with Deep Learning
  8. Natural Language Processing
  9. Feature Engineering & Model Evaluation

ADVANCED
  10. Reinforcement Learning
  11. MLOps & Model Deployment
  12. Generative AI & Diffusion Models
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass

os.environ.setdefault("DATABASE_URL", "sqlite:///./adaptive_learning.db")
os.environ.setdefault("SECRET_KEY", "seed-secret")

from app.core.database import SessionLocal, Base, engine
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.quiz import Quiz, Question

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ─────────────────────────────────────────────────────────────────────────────
COURSES = [

# ═══════════════════════════════════════════════════════════════════════════
# BEGINNER
# ═══════════════════════════════════════════════════════════════════════════

{
"title": "Python for AI & Data Science",
"description": "Learn Python from scratch with a focus on data manipulation, NumPy, Pandas, and writing clean ML-ready code.",
"difficulty": "beginner",
"category": "Programming",
"lessons": [
  {
    "title": "Python Basics & Data Types",
    "content": (
      "Python is the #1 language for AI and data science due to its simplicity and rich ecosystem.\n\n"
      "Core data types:\n"
      "• int, float — numbers\n"
      "• str — text strings\n"
      "• bool — True / False\n"
      "• list — ordered mutable collection: [1, 2, 3]\n"
      "• tuple — ordered immutable: (1, 2, 3)\n"
      "• dict — key-value pairs: {'name': 'Alice', 'age': 25}\n"
      "• set — unique unordered values: {1, 2, 3}\n\n"
      "Control flow:\n"
      "  if x > 0: print('positive')\n"
      "  for i in range(10): print(i)\n"
      "  while condition: do_something()\n\n"
      "Functions:\n"
      "  def add(a, b): return a + b\n"
      "  result = add(3, 4)  # 7\n\n"
      "List comprehensions (very common in ML code):\n"
      "  squares = [x**2 for x in range(10)]\n"
    ),
    "difficulty": "beginner",
    "order": 1,
    "quiz_title": "Python Basics Quiz",
    "questions": [
      {"text": "Which data type stores key-value pairs in Python?",
       "a": "list", "b": "tuple", "c": "dict", "d": "set", "ans": "C", "difficulty": "easy"},
      {"text": "What does len([1, 2, 3, 4]) return?",
       "a": "3", "b": "4", "c": "5", "d": "0", "ans": "B", "difficulty": "easy"},
      {"text": "Which keyword defines a function in Python?",
       "a": "func", "b": "function", "c": "def", "d": "lambda", "ans": "C", "difficulty": "easy"},
      {"text": "What is the output of: [x*2 for x in range(3)]?",
       "a": "[1,2,3]", "b": "[0,2,4]", "c": "[2,4,6]", "d": "[0,1,2]", "ans": "B", "difficulty": "medium"},
      {"text": "Which of these correctly creates a set in Python?",
       "a": "{}", "b": "set()", "c": "[]", "d": "()", "ans": "B", "difficulty": "medium"},
      {"text": "What does *args allow in a Python function?",
       "a": "Pass keyword arguments", "b": "Accept any number of positional arguments",
       "c": "Return multiple values", "d": "Create a generator", "ans": "B", "difficulty": "medium"},
      {"text": "What is a lambda function?",
       "a": "A function defined with the def keyword",
       "b": "An anonymous function defined in a single expression",
       "c": "A function that only accepts integers",
       "d": "A built-in Python class", "ans": "B", "difficulty": "hard"},
      {"text": "What does a Python generator do differently from a regular function?",
       "a": "It runs faster always",
       "b": "It yields values one at a time instead of returning all at once",
       "c": "It cannot accept arguments",
       "d": "It automatically parallelises execution", "ans": "B", "difficulty": "hard"},
    ],
  },
  {
    "title": "NumPy & Pandas for Data Science",
    "content": (
      "NumPy and Pandas are the two most important libraries for data work in Python.\n\n"
      "NumPy:\n"
      "  import numpy as np\n"
      "  arr = np.array([1, 2, 3, 4, 5])\n"
      "  arr.mean()   # 3.0\n"
      "  arr.reshape(5, 1)  # column vector\n"
      "  np.zeros((3,3)), np.ones((3,3)), np.eye(3)\n"
      "  Element-wise operations: arr * 2, arr + 10\n\n"
      "Pandas:\n"
      "  import pandas as pd\n"
      "  df = pd.read_csv('data.csv')\n"
      "  df.head(), df.describe(), df.shape\n"
      "  df['column'], df[df['age'] > 25]\n"
      "  df.groupby('category').mean()\n"
      "  df.dropna(), df.fillna(0)\n"
      "  df.merge(df2, on='id')\n\n"
      "These two libraries underpin nearly every ML pipeline."
    ),
    "difficulty": "beginner",
    "order": 2,
    "quiz_title": "NumPy & Pandas Quiz",
    "questions": [
      {"text": "What does np.array([1,2,3]).mean() return?",
       "a": "1", "b": "2.0", "c": "3", "d": "6", "ans": "B", "difficulty": "easy"},
      {"text": "Which Pandas method reads a CSV file into a DataFrame?",
       "a": "pd.load_csv()", "b": "pd.read_csv()", "c": "pd.open_csv()", "d": "pd.import_csv()", "ans": "B", "difficulty": "easy"},
      {"text": "What does df.head() display?",
       "a": "Column names only", "b": "Last 5 rows", "c": "First 5 rows", "d": "DataFrame shape", "ans": "C", "difficulty": "easy"},
      {"text": "How do you select rows where column 'age' is greater than 25 in a DataFrame df?",
       "a": "df.select(age > 25)", "b": "df[df['age'] > 25]",
       "c": "df.filter('age > 25')", "d": "df.query_age(25)", "ans": "B", "difficulty": "medium"},
      {"text": "What does df.dropna() do?",
       "a": "Drops columns with duplicate values",
       "b": "Removes rows containing NaN (missing) values",
       "c": "Fills NaN values with zero",
       "d": "Drops the last row", "ans": "B", "difficulty": "medium"},
      {"text": "What does np.reshape(arr, (2, 3)) require about the array size?",
       "a": "The array must have exactly 6 elements",
       "b": "The array must be sorted",
       "c": "The array must be a square matrix",
       "d": "The array must contain only integers", "ans": "A", "difficulty": "hard"},
      {"text": "What is broadcasting in NumPy?",
       "a": "Sending arrays over a network",
       "b": "NumPy's ability to perform operations on arrays of different shapes by stretching smaller arrays",
       "c": "Printing array values to console",
       "d": "Converting arrays to lists", "ans": "B", "difficulty": "hard"},
    ],
  },
]},

{
"title": "Mathematics for Machine Learning",
"description": "Linear algebra, calculus, probability and statistics — the mathematical foundations every ML practitioner needs.",
"difficulty": "beginner",
"category": "Mathematics",
"lessons": [
  {
    "title": "Linear Algebra Essentials",
    "content": (
      "Linear algebra is the language of machine learning. Almost every ML operation is a matrix computation.\n\n"
      "Key concepts:\n"
      "• Scalar — a single number (e.g. 5)\n"
      "• Vector — a 1D array of numbers [1, 2, 3]\n"
      "• Matrix — a 2D array of numbers\n"
      "• Tensor — a generalisation to N dimensions\n\n"
      "Operations:\n"
      "• Dot product: a·b = Σ aᵢbᵢ\n"
      "• Matrix multiplication: (m×n) · (n×p) = (m×p)\n"
      "• Transpose: Aᵀ flips rows and columns\n"
      "• Inverse: A·A⁻¹ = I (identity matrix)\n"
      "• Determinant: scalar value encoding how a matrix scales space\n\n"
      "Eigenvalues and eigenvectors: Av = λv\n"
      "• v is the eigenvector, λ is the eigenvalue\n"
      "• Used in PCA, Google PageRank, and spectral clustering"
    ),
    "difficulty": "beginner",
    "order": 1,
    "quiz_title": "Linear Algebra Quiz",
    "questions": [
      {"text": "What is a vector?",
       "a": "A 2D table of numbers", "b": "A single number",
       "c": "A 1D array of numbers", "d": "A mathematical function", "ans": "C", "difficulty": "easy"},
      {"text": "What does matrix multiplication require about the dimensions?",
       "a": "Both matrices must be square",
       "b": "The number of columns in the first matrix must equal the number of rows in the second",
       "c": "Both matrices must have the same shape",
       "d": "The matrices must be symmetric", "ans": "B", "difficulty": "easy"},
      {"text": "What does the transpose of a matrix do?",
       "a": "Inverts the matrix", "b": "Flips rows and columns",
       "c": "Computes the determinant", "d": "Multiplies all elements by -1", "ans": "B", "difficulty": "easy"},
      {"text": "What is the dot product of vectors [1,2] and [3,4]?",
       "a": "10", "b": "11", "c": "7", "d": "14", "ans": "B", "difficulty": "medium"},
      {"text": "If Av = λv, what is v called?",
       "a": "Eigenvalue", "b": "Determinant", "c": "Eigenvector", "d": "Gradient", "ans": "C", "difficulty": "medium"},
      {"text": "PCA (Principal Component Analysis) relies on which linear algebra concept?",
       "a": "Matrix determinant", "b": "Eigendecomposition of the covariance matrix",
       "c": "LU decomposition", "d": "Cross product", "ans": "B", "difficulty": "hard"},
      {"text": "What does a singular matrix mean?",
       "a": "It has all positive values",
       "b": "Its determinant is zero and it has no inverse",
       "c": "It is a 1×1 matrix",
       "d": "It is orthogonal", "ans": "B", "difficulty": "hard"},
    ],
  },
  {
    "title": "Probability & Statistics for ML",
    "content": (
      "Probability and statistics are fundamental to understanding and building ML models.\n\n"
      "Probability basics:\n"
      "• P(A) — probability of event A (0 to 1)\n"
      "• P(A|B) — conditional probability of A given B\n"
      "• Bayes' Theorem: P(A|B) = P(B|A)·P(A) / P(B)\n\n"
      "Distributions:\n"
      "• Normal (Gaussian): bell curve, defined by mean μ and std σ\n"
      "• Bernoulli: single binary trial\n"
      "• Binomial: n binary trials\n"
      "• Uniform: equal probability across range\n\n"
      "Statistics:\n"
      "• Mean — average\n"
      "• Median — middle value\n"
      "• Variance — spread: E[(X-μ)²]\n"
      "• Standard deviation — √variance\n"
      "• Correlation — linear relationship between two variables (-1 to 1)\n\n"
      "In ML: Naive Bayes uses Bayes' theorem; Gaussian distributions underlie many models."
    ),
    "difficulty": "beginner",
    "order": 2,
    "quiz_title": "Probability & Statistics Quiz",
    "questions": [
      {"text": "What is the range of a probability value?",
       "a": "-1 to 1", "b": "0 to 100", "c": "0 to 1", "d": "-∞ to ∞", "ans": "C", "difficulty": "easy"},
      {"text": "What does the mean represent?",
       "a": "The most frequent value", "b": "The middle value when sorted",
       "c": "The average of all values", "d": "The spread of data", "ans": "C", "difficulty": "easy"},
      {"text": "Standard deviation is the square root of:",
       "a": "Mean", "b": "Median", "c": "Variance", "d": "Correlation", "ans": "C", "difficulty": "easy"},
      {"text": "Bayes' Theorem computes:",
       "a": "The mean of a distribution",
       "b": "The conditional probability P(A|B) using P(B|A), P(A), and P(B)",
       "c": "The variance of a dataset",
       "d": "The eigenvalues of a covariance matrix", "ans": "B", "difficulty": "medium"},
      {"text": "A correlation coefficient of -1 indicates:",
       "a": "No relationship", "b": "A perfect positive linear relationship",
       "c": "A perfect negative linear relationship", "d": "A non-linear relationship", "ans": "C", "difficulty": "medium"},
      {"text": "Which distribution describes the outcome of a single coin flip?",
       "a": "Normal", "b": "Poisson", "c": "Bernoulli", "d": "Exponential", "ans": "C", "difficulty": "medium"},
      {"text": "In the context of ML, what is the Maximum Likelihood Estimation (MLE)?",
       "a": "Choosing model parameters that maximise the probability of observing the training data",
       "b": "Selecting the largest eigenvalue",
       "c": "Computing the maximum gradient during training",
       "d": "Picking the highest accuracy on the test set", "ans": "A", "difficulty": "hard"},
      {"text": "What does a p-value less than 0.05 typically indicate in hypothesis testing?",
       "a": "The null hypothesis is definitely true",
       "b": "There is strong evidence to reject the null hypothesis",
       "c": "The model is overfitting",
       "d": "The dataset is too small", "ans": "B", "difficulty": "hard"},
    ],
  },
]},

{
"title": "Data Analysis & Visualisation",
"description": "Explore, clean, and visualise data using Matplotlib, Seaborn, and Pandas to extract insights before building ML models.",
"difficulty": "beginner",
"category": "Data Science",
"lessons": [
  {
    "title": "Exploratory Data Analysis (EDA)",
    "content": (
      "EDA is the first step in any ML project — understanding your data before modelling.\n\n"
      "Key EDA steps:\n"
      "1. Load data: pd.read_csv('file.csv')\n"
      "2. Inspect shape: df.shape, df.dtypes, df.head()\n"
      "3. Summary statistics: df.describe()\n"
      "4. Check missing values: df.isnull().sum()\n"
      "5. Check duplicates: df.duplicated().sum()\n"
      "6. Distribution of target variable\n"
      "7. Correlation matrix: df.corr()\n\n"
      "Data quality issues to look for:\n"
      "• Missing values (NaN)\n"
      "• Outliers (values far from the mean)\n"
      "• Incorrect data types\n"
      "• Class imbalance in classification targets\n"
      "• Duplicate rows"
    ),
    "difficulty": "beginner",
    "order": 1,
    "quiz_title": "EDA Quiz",
    "questions": [
      {"text": "What does df.shape return for a DataFrame?",
       "a": "Column names", "b": "Number of rows and columns as a tuple",
       "c": "Data types of each column", "d": "Summary statistics", "ans": "B", "difficulty": "easy"},
      {"text": "Which method checks for missing values in a Pandas DataFrame?",
       "a": "df.missing()", "b": "df.null_check()", "c": "df.isnull().sum()", "d": "df.na()", "ans": "C", "difficulty": "easy"},
      {"text": "What does df.describe() provide?",
       "a": "A list of column names",
       "b": "Count, mean, std, min, max and percentiles for numeric columns",
       "c": "A plot of the data distribution",
       "d": "The number of unique values per column", "ans": "B", "difficulty": "easy"},
      {"text": "What is an outlier in a dataset?",
       "a": "A duplicate row",
       "b": "A value that lies far from most other values in the data",
       "c": "A missing value",
       "d": "A categorical variable", "ans": "B", "difficulty": "medium"},
      {"text": "A correlation matrix value close to 1 between two features means:",
       "a": "They are unrelated", "b": "They have a strong positive linear relationship",
       "c": "One causes the other", "d": "They should both be dropped", "ans": "B", "difficulty": "medium"},
      {"text": "Class imbalance in a classification dataset means:",
       "a": "The dataset has missing values",
       "b": "One class has many more samples than others",
       "c": "All features have the same scale",
       "d": "The dataset has too many features", "ans": "B", "difficulty": "hard"},
      {"text": "Which technique helps handle outliers without removing data points?",
       "a": "One-hot encoding", "b": "Winsorisation (capping extreme values at a percentile)",
       "c": "Label encoding", "d": "StandardScaler", "ans": "B", "difficulty": "hard"},
    ],
  },
  {
    "title": "Data Visualisation with Matplotlib & Seaborn",
    "content": (
      "Visualisation turns raw numbers into insight. Python's two main viz libraries:\n\n"
      "Matplotlib (low-level, full control):\n"
      "  import matplotlib.pyplot as plt\n"
      "  plt.plot(x, y)          # line chart\n"
      "  plt.bar(categories, values)  # bar chart\n"
      "  plt.scatter(x, y)       # scatter plot\n"
      "  plt.hist(data, bins=20) # histogram\n"
      "  plt.show()\n\n"
      "Seaborn (high-level, statistical plots):\n"
      "  import seaborn as sns\n"
      "  sns.heatmap(df.corr(), annot=True)   # correlation heatmap\n"
      "  sns.boxplot(x='category', y='value', data=df)\n"
      "  sns.pairplot(df)                     # pairwise scatter plots\n"
      "  sns.histplot(df['column'], kde=True) # distribution with KDE\n\n"
      "Choosing the right chart:\n"
      "• Distribution → histogram, KDE, boxplot\n"
      "• Relationship → scatter plot, heatmap\n"
      "• Comparison → bar chart, grouped bar\n"
      "• Trend over time → line chart"
    ),
    "difficulty": "beginner",
    "order": 2,
    "quiz_title": "Data Visualisation Quiz",
    "questions": [
      {"text": "Which plot is best for showing the distribution of a single continuous variable?",
       "a": "Bar chart", "b": "Scatter plot", "c": "Histogram", "d": "Pie chart", "ans": "C", "difficulty": "easy"},
      {"text": "What does a scatter plot show?",
       "a": "Category counts", "b": "Relationship between two continuous variables",
       "c": "Time series trends", "d": "Feature importance", "ans": "B", "difficulty": "easy"},
      {"text": "Which Seaborn function creates a correlation heatmap?",
       "a": "sns.scatter()", "b": "sns.corr()", "c": "sns.heatmap(df.corr())", "d": "sns.matrix()", "ans": "C", "difficulty": "easy"},
      {"text": "A boxplot shows all of the following EXCEPT:",
       "a": "Median", "b": "Interquartile range", "c": "Outliers", "d": "Exact data values", "ans": "D", "difficulty": "medium"},
      {"text": "What does a KDE (Kernel Density Estimate) plot show?",
       "a": "A bar chart of categories",
       "b": "A smooth continuous estimate of the probability distribution of a variable",
       "c": "Correlations between features",
       "d": "Model accuracy over epochs", "ans": "B", "difficulty": "medium"},
      {"text": "When should you use a log scale on an axis?",
       "a": "When all values are negative",
       "b": "When data spans several orders of magnitude",
       "c": "When there are fewer than 10 data points",
       "d": "When the data is normally distributed", "ans": "B", "difficulty": "hard"},
      {"text": "What does sns.pairplot(df) produce?",
       "a": "A single scatter plot", "b": "A heatmap of missing values",
       "c": "A grid of scatter plots for each pair of numerical features",
       "d": "A bar chart for each categorical column", "ans": "C", "difficulty": "hard"},
    ],
  },
]},

# ═══════════════════════════════════════════════════════════════════════════
# INTERMEDIATE
# ═══════════════════════════════════════════════════════════════════════════

{
"title": "Computer Vision with Deep Learning",
"description": "Build image classifiers, object detectors, and image segmentation models using CNNs and modern architectures.",
"difficulty": "intermediate",
"category": "Computer Vision",
"lessons": [
  {
    "title": "Convolutional Neural Networks (CNNs)",
    "content": (
      "CNNs are the backbone of computer vision. Unlike fully connected networks, CNNs use spatial structure.\n\n"
      "Key layers:\n"
      "• Convolutional layer — applies learned filters to extract features (edges, textures, shapes)\n"
      "  Output size = (W - F + 2P) / S + 1  where W=input, F=filter, P=padding, S=stride\n"
      "• Activation — ReLU after each convolution\n"
      "• Pooling layer — reduces spatial dimensions (Max pooling most common)\n"
      "• Fully Connected (Dense) layer — final classification\n"
      "• Softmax — outputs class probabilities\n\n"
      "Famous architectures:\n"
      "• LeNet-5 (1998) — first successful CNN\n"
      "• AlexNet (2012) — deep learning breakthrough\n"
      "• VGG16/19 — deep uniform architecture\n"
      "• ResNet — residual connections, 152 layers\n"
      "• EfficientNet — compound scaling\n\n"
      "Transfer learning: use pretrained weights (ImageNet) and fine-tune on your task."
    ),
    "difficulty": "intermediate",
    "order": 1,
    "quiz_title": "CNN Quiz",
    "questions": [
      {"text": "What is the primary purpose of a convolutional layer?",
       "a": "To reduce the number of classes",
       "b": "To extract spatial features using learned filters",
       "c": "To normalise pixel values",
       "d": "To convert images to grayscale", "ans": "B", "difficulty": "easy"},
      {"text": "Max pooling is used to:",
       "a": "Increase image resolution", "b": "Add noise to prevent overfitting",
       "c": "Reduce spatial dimensions while keeping dominant features", "d": "Apply batch normalisation", "ans": "C", "difficulty": "easy"},
      {"text": "What is transfer learning in computer vision?",
       "a": "Training a CNN from scratch on a new dataset",
       "b": "Using weights pretrained on a large dataset as a starting point for a new task",
       "c": "Converting a CNN to an RNN",
       "d": "Transferring images between servers", "ans": "B", "difficulty": "medium"},
      {"text": "ResNet introduced residual connections to solve which problem?",
       "a": "Slow inference speed",
       "b": "The vanishing gradient problem in very deep networks",
       "c": "Overfitting on small datasets",
       "d": "Large memory usage", "ans": "B", "difficulty": "medium"},
      {"text": "What does a stride of 2 in a convolutional layer do?",
       "a": "Doubles the filter size",
       "b": "Moves the filter 2 pixels at a time, reducing output size",
       "c": "Applies two filters simultaneously",
       "d": "Adds 2 pixels of padding", "ans": "B", "difficulty": "medium"},
      {"text": "In a CNN, what does the depth of a feature map represent?",
       "a": "Image height in pixels",
       "b": "The number of filters applied, each detecting a different feature",
       "c": "The number of training examples",
       "d": "The batch size", "ans": "B", "difficulty": "hard"},
      {"text": "What is data augmentation in the context of image training?",
       "a": "Adding more labels to the dataset",
       "b": "Artificially expanding training data with transformations like flips, rotations, and crops",
       "c": "Increasing image resolution",
       "d": "Balancing class distribution by removing samples", "ans": "B", "difficulty": "hard"},
    ],
  },
  {
    "title": "Object Detection & Image Segmentation",
    "content": (
      "Beyond classification — locating and segmenting objects in images.\n\n"
      "Object Detection:\n"
      "• Task: find objects and draw bounding boxes around them\n"
      "• Metrics: mAP (mean Average Precision), IoU (Intersection over Union)\n"
      "• Algorithms:\n"
      "  - YOLO (You Only Look Once) — real-time, single-pass detection\n"
      "  - Faster R-CNN — region proposals + CNN, very accurate\n"
      "  - SSD (Single Shot Detector) — fast, multi-scale\n\n"
      "Image Segmentation:\n"
      "• Semantic segmentation — label every pixel with a class\n"
      "• Instance segmentation — distinguish individual object instances\n"
      "• Key model: U-Net (encoder-decoder with skip connections)\n"
      "• Mask R-CNN — extends Faster R-CNN with pixel masks\n\n"
      "IoU = Area of Overlap / Area of Union\n"
      "A prediction with IoU > 0.5 is typically considered a True Positive."
    ),
    "difficulty": "intermediate",
    "order": 2,
    "quiz_title": "Object Detection Quiz",
    "questions": [
      {"text": "What does YOLO stand for?",
       "a": "You Only Learn Once", "b": "You Only Look Once",
       "c": "Your Object Localisation Output", "d": "Yellow Orange Label Object", "ans": "B", "difficulty": "easy"},
      {"text": "IoU (Intersection over Union) measures:",
       "a": "Model accuracy on a test set",
       "b": "The overlap between a predicted bounding box and the ground truth",
       "c": "The ratio of true positives to false positives",
       "d": "Training loss convergence", "ans": "B", "difficulty": "medium"},
      {"text": "What is semantic segmentation?",
       "a": "Classifying entire images into categories",
       "b": "Assigning a class label to every pixel in an image",
       "c": "Drawing bounding boxes around objects",
       "d": "Detecting objects in video streams", "ans": "B", "difficulty": "medium"},
      {"text": "U-Net is widely used for:",
       "a": "Text generation", "b": "Image classification on ImageNet",
       "c": "Medical image segmentation", "d": "Object tracking in video", "ans": "C", "difficulty": "medium"},
      {"text": "What distinguishes instance segmentation from semantic segmentation?",
       "a": "Instance segmentation only classifies the background",
       "b": "Instance segmentation identifies individual object instances separately, not just pixel classes",
       "c": "Semantic segmentation uses bounding boxes",
       "d": "Instance segmentation works only on grayscale images", "ans": "B", "difficulty": "hard"},
      {"text": "mAP (mean Average Precision) in object detection is calculated by:",
       "a": "Averaging the IoU across all detections",
       "b": "Averaging the precision-recall area under curve across all object classes",
       "c": "Taking the mean of all confidence scores",
       "d": "Dividing total true positives by total images", "ans": "B", "difficulty": "hard"},
    ],
  },
]},

{
"title": "Natural Language Processing",
"description": "Teach machines to understand and generate text — from tokenisation and word embeddings to BERT and text classification.",
"difficulty": "intermediate",
"category": "NLP",
"lessons": [
  {
    "title": "Text Preprocessing & Word Embeddings",
    "content": (
      "Before feeding text to a model, it must be converted to numbers.\n\n"
      "Text preprocessing pipeline:\n"
      "1. Tokenisation — split text into tokens (words or subwords)\n"
      "2. Lowercasing — reduce vocabulary size\n"
      "3. Stop word removal — remove common words (the, is, at)\n"
      "4. Stemming/Lemmatisation — reduce words to root form\n"
      "5. Vectorisation — convert tokens to numbers\n\n"
      "Bag of Words (BoW):\n"
      "  Represents text as word frequency counts. Ignores order.\n\n"
      "TF-IDF (Term Frequency–Inverse Document Frequency):\n"
      "  Weights words by how unique they are across documents.\n"
      "  TF-IDF = TF × log(N/df)\n\n"
      "Word Embeddings:\n"
      "• Word2Vec — learns dense vector representations from context\n"
      "  - CBOW: predict word from context\n"
      "  - Skip-gram: predict context from word\n"
      "• GloVe — global co-occurrence statistics\n"
      "• FastText — handles subword information\n"
      "Similar words have similar vectors: king - man + woman ≈ queen"
    ),
    "difficulty": "intermediate",
    "order": 1,
    "quiz_title": "NLP Preprocessing Quiz",
    "questions": [
      {"text": "What is tokenisation in NLP?",
       "a": "Translating text to another language",
       "b": "Splitting text into smaller units like words or subwords",
       "c": "Removing punctuation from text",
       "d": "Converting text to lowercase", "ans": "B", "difficulty": "easy"},
      {"text": "What does TF-IDF measure?",
       "a": "Sentence grammar correctness",
       "b": "How important a word is in a document relative to a collection of documents",
       "c": "The number of sentences in a document",
       "d": "Spelling accuracy", "ans": "B", "difficulty": "easy"},
      {"text": "Word2Vec represents words as:",
       "a": "One-hot encoded sparse vectors",
       "b": "Dense low-dimensional vectors capturing semantic meaning",
       "c": "Frequency count integers",
       "d": "Binary sequences", "ans": "B", "difficulty": "medium"},
      {"text": "Lemmatisation differs from stemming because:",
       "a": "Lemmatisation is faster",
       "b": "Lemmatisation returns the dictionary base form; stemming just chops suffixes",
       "c": "Stemming uses a dictionary lookup",
       "d": "Lemmatisation removes stop words", "ans": "B", "difficulty": "medium"},
      {"text": "What does the analogy 'king - man + woman ≈ queen' demonstrate about word embeddings?",
       "a": "Word embeddings memorise training sentences",
       "b": "Semantic relationships are encoded as directions in the embedding space",
       "c": "All words have the same vector length",
       "d": "Word2Vec was trained on royalty data", "ans": "B", "difficulty": "hard"},
      {"text": "What is the main limitation of Bag-of-Words (BoW)?",
       "a": "It requires GPU training",
       "b": "It ignores word order and context",
       "c": "It can only handle sentences under 10 words",
       "d": "It cannot handle punctuation", "ans": "B", "difficulty": "hard"},
    ],
  },
  {
    "title": "Text Classification & Sentiment Analysis",
    "content": (
      "Text classification assigns a label to a piece of text. Sentiment analysis is a specific case.\n\n"
      "Classic ML approaches:\n"
      "• Naive Bayes — probabilistic, fast, works well on text\n"
      "• Logistic Regression with TF-IDF features\n"
      "• SVM with text features\n\n"
      "Deep learning approaches:\n"
      "• RNN / LSTM — process sequences with memory\n"
      "• TextCNN — 1D convolutions over text\n"
      "• BERT fine-tuning — state-of-the-art for most classification tasks\n\n"
      "Sentiment Analysis:\n"
      "• Binary: positive / negative\n"
      "• Multi-class: very negative / negative / neutral / positive / very positive\n"
      "• Aspect-based: sentiment towards specific aspects (food, service, price)\n\n"
      "Evaluation metrics:\n"
      "• Accuracy — overall correct / total\n"
      "• Precision — TP / (TP + FP)\n"
      "• Recall — TP / (TP + FN)\n"
      "• F1 Score — harmonic mean of precision and recall\n"
      "• Confusion matrix"
    ),
    "difficulty": "intermediate",
    "order": 2,
    "quiz_title": "Text Classification Quiz",
    "questions": [
      {"text": "Sentiment analysis classifies:",
       "a": "Named entities in text",
       "b": "The emotional tone or opinion expressed in text",
       "c": "The language a document is written in",
       "d": "Grammar errors in sentences", "ans": "B", "difficulty": "easy"},
      {"text": "F1 Score is the harmonic mean of:",
       "a": "Accuracy and loss", "b": "Precision and recall",
       "c": "Sensitivity and specificity", "d": "Training and test accuracy", "ans": "B", "difficulty": "easy"},
      {"text": "Why is Naive Bayes commonly used for text classification?",
       "a": "It uses deep learning",
       "b": "It is fast, works well with high-dimensional sparse text features, and needs little data",
       "c": "It automatically removes stop words",
       "d": "It is the most accurate classifier", "ans": "B", "difficulty": "medium"},
      {"text": "BERT achieves strong text classification results because:",
       "a": "It uses a recurrent architecture",
       "b": "It is pre-trained on massive text and understands bidirectional context",
       "c": "It has fewer parameters than LSTM",
       "d": "It was trained specifically for sentiment", "ans": "B", "difficulty": "medium"},
      {"text": "Which metric is most appropriate when false negatives are very costly (e.g. cancer detection)?",
       "a": "Accuracy", "b": "Precision", "c": "Recall", "d": "Specificity", "ans": "C", "difficulty": "hard"},
      {"text": "What does a confusion matrix show?",
       "a": "Training loss over epochs",
       "b": "Counts of true positives, true negatives, false positives, and false negatives",
       "c": "Feature importance scores",
       "d": "Hyperparameter search results", "ans": "B", "difficulty": "hard"},
    ],
  },
]},

{
"title": "Feature Engineering & Model Evaluation",
"description": "Master the art of creating powerful features and rigorously evaluating ML models to avoid common pitfalls.",
"difficulty": "intermediate",
"category": "Machine Learning",
"lessons": [
  {
    "title": "Feature Engineering Techniques",
    "content": (
      "Feature engineering is often more impactful than choosing a better algorithm.\n\n"
      "Encoding categorical variables:\n"
      "• Label Encoding — integer mapping (cat=0, dog=1)\n"
      "  Risk: implies ordinal relationship where none exists\n"
      "• One-Hot Encoding — binary column per category\n"
      "  Drawback: high cardinality → curse of dimensionality\n"
      "• Target Encoding — replace category with mean target value\n\n"
      "Scaling numerical features:\n"
      "• StandardScaler: z = (x - μ) / σ  → mean=0, std=1\n"
      "• MinMaxScaler: x' = (x - min) / (max - min) → range [0,1]\n"
      "• RobustScaler: uses median and IQR, robust to outliers\n\n"
      "Feature creation:\n"
      "• Polynomial features: x₁², x₁·x₂\n"
      "• Date features: day of week, month, is_weekend\n"
      "• Aggregations: mean, std, min, max per group\n"
      "• Interaction terms\n\n"
      "Feature selection:\n"
      "• Correlation filter\n"
      "• Feature importance from tree models\n"
      "• Recursive Feature Elimination (RFE)\n"
      "• L1 regularisation (LASSO)"
    ),
    "difficulty": "intermediate",
    "order": 1,
    "quiz_title": "Feature Engineering Quiz",
    "questions": [
      {"text": "What is one-hot encoding used for?",
       "a": "Scaling numerical features to [0,1]",
       "b": "Converting categorical variables into binary columns",
       "c": "Removing missing values",
       "d": "Creating polynomial features", "ans": "B", "difficulty": "easy"},
      {"text": "StandardScaler transforms features to have:",
       "a": "Values between 0 and 1",
       "b": "Mean 0 and standard deviation 1",
       "c": "Only positive values",
       "d": "Integer values", "ans": "B", "difficulty": "easy"},
      {"text": "When should you use RobustScaler instead of StandardScaler?",
       "a": "When the dataset is very large",
       "b": "When the data contains significant outliers",
       "c": "When features are already normalised",
       "d": "When training a neural network", "ans": "B", "difficulty": "medium"},
      {"text": "What is the risk of using label encoding for a non-ordinal categorical variable?",
       "a": "It creates too many columns",
       "b": "The model may incorrectly interpret the integer values as an ordered relationship",
       "c": "It cannot handle missing values",
       "d": "It increases training time significantly", "ans": "B", "difficulty": "medium"},
      {"text": "LASSO regression performs feature selection because:",
       "a": "It removes correlated features before training",
       "b": "L1 regularisation can shrink some feature weights exactly to zero",
       "c": "It uses a decision tree internally",
       "d": "It applies PCA automatically", "ans": "B", "difficulty": "hard"},
      {"text": "What is target encoding and when can it cause data leakage?",
       "a": "Encoding labels as integers; leakage occurs with large categories",
       "b": "Replacing a category with its mean target value; leakage if computed on the full dataset before splitting",
       "c": "Normalising the target variable; leakage when test set is small",
       "d": "One-hot encoding the target; leakage when classes are imbalanced", "ans": "B", "difficulty": "hard"},
    ],
  },
  {
    "title": "Model Evaluation & Hyperparameter Tuning",
    "content": (
      "Building a model is only half the work — evaluating and tuning it correctly is critical.\n\n"
      "Train / Validation / Test split:\n"
      "• Typical: 70% train, 15% validation, 15% test\n"
      "• Never touch the test set until final evaluation\n\n"
      "Cross-validation:\n"
      "• k-Fold CV — split data into k folds, train on k-1, test on 1, rotate k times\n"
      "• Stratified k-Fold — preserves class distribution in each fold\n\n"
      "Evaluation metrics by task:\n"
      "• Classification: accuracy, precision, recall, F1, AUC-ROC\n"
      "• Regression: MAE, MSE, RMSE, R²\n\n"
      "Hyperparameter tuning:\n"
      "• Grid Search — exhaustive search over a parameter grid\n"
      "• Random Search — randomly sample parameter combinations\n"
      "• Bayesian Optimisation — use prior results to guide search (most efficient)\n"
      "• Optuna, Ray Tune — popular libraries\n\n"
      "Learning curves: plot training and validation loss vs training size to diagnose\n"
      "bias (underfitting) vs variance (overfitting)."
    ),
    "difficulty": "intermediate",
    "order": 2,
    "quiz_title": "Model Evaluation Quiz",
    "questions": [
      {"text": "What is the purpose of the test set?",
       "a": "To tune hyperparameters",
       "b": "To provide a final unbiased estimate of model performance",
       "c": "To train the final model",
       "d": "To remove outliers", "ans": "B", "difficulty": "easy"},
      {"text": "AUC-ROC measures:",
       "a": "Mean squared error of predictions",
       "b": "The model's ability to distinguish between classes across all classification thresholds",
       "c": "Feature importance ranking",
       "d": "Training time vs accuracy", "ans": "B", "difficulty": "medium"},
      {"text": "What does k-Fold cross-validation help with?",
       "a": "Reducing training time",
       "b": "Getting a more reliable estimate of model performance by using all data for both training and validation",
       "c": "Automatically selecting features",
       "d": "Handling class imbalance", "ans": "B", "difficulty": "medium"},
      {"text": "Which hyperparameter tuning method is most computationally expensive?",
       "a": "Random Search", "b": "Bayesian Optimisation",
       "c": "Grid Search", "d": "Manual tuning", "ans": "C", "difficulty": "medium"},
      {"text": "A model with high bias and low variance is:",
       "a": "Overfitting", "b": "Well-calibrated",
       "c": "Underfitting — too simple to capture the patterns in the data", "d": "Overparameterised", "ans": "C", "difficulty": "hard"},
      {"text": "R² (coefficient of determination) in regression equals 1 when:",
       "a": "The model predicts the mean for all inputs",
       "b": "The model perfectly predicts all target values",
       "c": "The model has only one feature",
       "d": "RMSE is minimised to zero", "ans": "B", "difficulty": "hard"},
    ],
  },
]},

# ═══════════════════════════════════════════════════════════════════════════
# ADVANCED
# ═══════════════════════════════════════════════════════════════════════════

{
"title": "Reinforcement Learning",
"description": "Learn how agents learn through trial and error — Q-learning, policy gradients, PPO, and real-world RL applications.",
"difficulty": "advanced",
"category": "Reinforcement Learning",
"lessons": [
  {
    "title": "RL Fundamentals: MDP, Q-Learning & DQN",
    "content": (
      "Reinforcement Learning (RL) trains an agent to maximise cumulative reward through interaction with an environment.\n\n"
      "Core concepts:\n"
      "• Agent — the learner/decision maker\n"
      "• Environment — what the agent interacts with\n"
      "• State (s) — current situation\n"
      "• Action (a) — what the agent does\n"
      "• Reward (r) — feedback signal\n"
      "• Policy π(s) — mapping from states to actions\n"
      "• Value function V(s) — expected cumulative reward from state s\n"
      "• Q-function Q(s,a) — expected cumulative reward from taking action a in state s\n\n"
      "Markov Decision Process (MDP):\n"
      "  Defined by (S, A, P, R, γ)\n"
      "  γ (discount factor) — how much future rewards are valued\n\n"
      "Q-Learning:\n"
      "  Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]\n"
      "  Converges to optimal policy for finite MDPs\n\n"
      "DQN (Deep Q-Network):\n"
      "  Replaces Q-table with a neural network\n"
      "  Experience replay + target network for stability\n"
      "  Achieved human-level performance on Atari games (DeepMind, 2013)"
    ),
    "difficulty": "advanced",
    "order": 1,
    "quiz_title": "RL Fundamentals Quiz",
    "questions": [
      {"text": "In reinforcement learning, the agent tries to maximise:",
       "a": "The loss function", "b": "Cumulative reward over time",
       "c": "The number of actions taken", "d": "The entropy of its policy", "ans": "B", "difficulty": "easy"},
      {"text": "What does the discount factor γ control in RL?",
       "a": "The learning rate of the neural network",
       "b": "How much weight the agent places on future rewards vs immediate rewards",
       "c": "The number of episodes to train for",
       "d": "The size of the replay buffer", "ans": "B", "difficulty": "medium"},
      {"text": "What is a policy in reinforcement learning?",
       "a": "The reward function",
       "b": "A mapping from states to actions that the agent follows",
       "c": "The environment's transition dynamics",
       "d": "The neural network architecture", "ans": "B", "difficulty": "medium"},
      {"text": "DQN improves over basic Q-learning by:",
       "a": "Using a simpler environment",
       "b": "Replacing the Q-table with a neural network and using experience replay and a target network",
       "c": "Removing the discount factor",
       "d": "Only learning from positive rewards", "ans": "B", "difficulty": "hard"},
      {"text": "What is the exploration-exploitation trade-off in RL?",
       "a": "Balancing training time vs inference speed",
       "b": "Choosing between trying new actions (explore) and using the best-known action (exploit)",
       "c": "Balancing the size of the neural network vs dataset size",
       "d": "Deciding whether to use model-based or model-free RL", "ans": "B", "difficulty": "hard"},
      {"text": "The Bellman equation in Q-learning expresses:",
       "a": "The gradient of the loss with respect to model weights",
       "b": "The recursive relationship between the Q-value of a state-action pair and the next state's Q-value",
       "c": "The probability of transitioning between states",
       "d": "The optimal neural network architecture for RL", "ans": "B", "difficulty": "hard"},
    ],
  },
  {
    "title": "Policy Gradient Methods & Modern RL",
    "content": (
      "Policy gradient methods optimise the policy directly instead of learning a value function.\n\n"
      "REINFORCE algorithm:\n"
      "  ∇J(θ) = E[∇log π_θ(a|s) · G_t]\n"
      "  Updates policy parameters using the return G_t\n"
      "  High variance — slow convergence\n\n"
      "Actor-Critic methods:\n"
      "  Actor: learns the policy\n"
      "  Critic: learns the value function to reduce variance\n"
      "  A3C (Asynchronous Advantage Actor-Critic)\n\n"
      "PPO (Proximal Policy Optimisation):\n"
      "  State-of-the-art for continuous control and games\n"
      "  Clips policy updates to prevent too-large changes\n"
      "  Used to train ChatGPT (via RLHF)\n\n"
      "RLHF (Reinforcement Learning from Human Feedback):\n"
      "  Reward model trained on human preference data\n"
      "  PPO fine-tunes LLMs to align with human preferences\n\n"
      "Applications: robotics, game playing (AlphaGo, OpenAI Five), autonomous driving, recommendation systems"
    ),
    "difficulty": "advanced",
    "order": 2,
    "quiz_title": "Policy Gradients Quiz",
    "questions": [
      {"text": "What does PPO stand for?",
       "a": "Partial Policy Optimisation", "b": "Proximal Policy Optimisation",
       "c": "Parallel Processing Optimiser", "d": "Parametric Policy Output", "ans": "B", "difficulty": "easy"},
      {"text": "In Actor-Critic methods, the Critic's role is to:",
       "a": "Select the best action at each step",
       "b": "Estimate the value function to reduce variance in policy gradient updates",
       "c": "Collect experience from the environment",
       "d": "Apply regularisation to the policy", "ans": "B", "difficulty": "medium"},
      {"text": "RLHF (Reinforcement Learning from Human Feedback) is used to:",
       "a": "Train agents in video games",
       "b": "Align LLMs with human preferences by training a reward model on human comparisons",
       "c": "Speed up training on robotic tasks",
       "d": "Replace the actor network with human demonstrations", "ans": "B", "difficulty": "hard"},
      {"text": "Why does PPO clip the policy update ratio?",
       "a": "To speed up training",
       "b": "To prevent overly large policy updates that could destabilise training",
       "c": "To reduce memory usage",
       "d": "To enforce exploration", "ans": "B", "difficulty": "hard"},
      {"text": "What distinguishes model-based RL from model-free RL?",
       "a": "Model-based RL uses neural networks; model-free does not",
       "b": "Model-based RL learns a model of the environment and plans with it; model-free learns directly from experience",
       "c": "Model-free RL is always more sample-efficient",
       "d": "Model-based RL can only be used in simulation", "ans": "B", "difficulty": "hard"},
    ],
  },
]},

{
"title": "MLOps & Model Deployment",
"description": "Take ML models from notebook to production: experiment tracking, CI/CD for ML, containerisation, serving, and monitoring.",
"difficulty": "advanced",
"category": "MLOps",
"lessons": [
  {
    "title": "Experiment Tracking & ML Pipelines",
    "content": (
      "MLOps bridges the gap between ML experimentation and reliable production systems.\n\n"
      "Experiment tracking:\n"
      "• MLflow — open-source, tracks parameters, metrics, and artifacts\n"
      "  mlflow.log_param('lr', 0.01)\n"
      "  mlflow.log_metric('accuracy', 0.95)\n"
      "  mlflow.sklearn.log_model(model, 'model')\n"
      "• Weights & Biases (wandb) — collaborative experiment tracking\n"
      "• DVC (Data Version Control) — version datasets and models\n\n"
      "ML Pipelines:\n"
      "• Scikit-learn Pipeline — chains preprocessing + model steps\n"
      "  pipe = Pipeline([('scaler', StandardScaler()), ('clf', SVC())])\n"
      "• Kubeflow, Apache Airflow, ZenML — production ML orchestration\n\n"
      "Feature stores:\n"
      "• Centralise feature computation and serving\n"
      "• Examples: Feast, Tecton, Hopsworks\n"
      "• Prevents training-serving skew\n\n"
      "Model registry:\n"
      "• Version and stage models (staging → production)\n"
      "• MLflow Model Registry, SageMaker Model Registry"
    ),
    "difficulty": "advanced",
    "order": 1,
    "quiz_title": "MLOps Fundamentals Quiz",
    "questions": [
      {"text": "What is the main purpose of experiment tracking tools like MLflow?",
       "a": "To deploy models to production automatically",
       "b": "To log, compare, and reproduce ML experiments by tracking parameters, metrics, and artefacts",
       "c": "To visualise neural network architectures",
       "d": "To manage database schemas", "ans": "B", "difficulty": "easy"},
      {"text": "What is training-serving skew?",
       "a": "A difference in model accuracy between GPU and CPU",
       "b": "Discrepancies between features used during training and features available at serving time",
       "c": "Slow model inference in production",
       "d": "A difference between train and test dataset sizes", "ans": "B", "difficulty": "medium"},
      {"text": "A Scikit-learn Pipeline is useful because:",
       "a": "It automatically selects the best algorithm",
       "b": "It chains preprocessing and modelling steps, preventing data leakage and simplifying deployment",
       "c": "It trains models in parallel",
       "d": "It works only with neural networks", "ans": "B", "difficulty": "medium"},
      {"text": "What does DVC (Data Version Control) primarily manage?",
       "a": "Model hyperparameters", "b": "Large datasets and model files with Git-like versioning",
       "c": "Production server configuration", "d": "Feature importance scores", "ans": "B", "difficulty": "hard"},
      {"text": "A model registry in MLOps provides:",
       "a": "A place to store raw training data",
       "b": "Centralised versioning, staging, and lifecycle management for ML models",
       "c": "Automatic hyperparameter tuning",
       "d": "Real-time feature computation", "ans": "B", "difficulty": "hard"},
    ],
  },
  {
    "title": "Model Serving, Monitoring & CI/CD for ML",
    "content": (
      "Deploying a model is just the beginning — it needs to be served reliably and monitored continuously.\n\n"
      "Model serving options:\n"
      "• REST API (FastAPI, Flask) — custom HTTP endpoint\n"
      "• TorchServe / TensorFlow Serving — framework-specific servers\n"
      "• Triton Inference Server — NVIDIA, multi-framework, GPU-optimised\n"
      "• BentoML, Seldon Core — ML-specific serving platforms\n"
      "• Serverless: AWS Lambda, Google Cloud Functions\n\n"
      "Containerisation:\n"
      "• Docker — package model + dependencies into a portable image\n"
      "• Kubernetes — orchestrate containers at scale\n\n"
      "Model monitoring:\n"
      "• Data drift — input distribution shifts over time\n"
      "• Concept drift — relationship between features and target changes\n"
      "• Performance monitoring — track accuracy, latency, error rates\n"
      "• Tools: Evidently AI, Arize, WhyLabs\n\n"
      "CI/CD for ML:\n"
      "• Continuous Integration — automated testing of code and model quality\n"
      "• Continuous Delivery — automated deployment to staging/production\n"
      "• GitHub Actions, Jenkins, GitLab CI commonly used"
    ),
    "difficulty": "advanced",
    "order": 2,
    "quiz_title": "Model Serving & Monitoring Quiz",
    "questions": [
      {"text": "What is data drift in ML monitoring?",
       "a": "A bug in the data pipeline",
       "b": "The statistical distribution of input features changing over time compared to training data",
       "c": "Gradual increase in model file size",
       "d": "Slow database query performance", "ans": "B", "difficulty": "medium"},
      {"text": "What is concept drift?",
       "a": "A change in the server infrastructure",
       "b": "The statistical relationship between input features and the target variable changing over time",
       "c": "The model architecture becoming outdated",
       "d": "A decrease in dataset size", "ans": "B", "difficulty": "medium"},
      {"text": "Why is containerising ML models with Docker beneficial for deployment?",
       "a": "It trains models faster",
       "b": "It packages the model and all dependencies into a portable, reproducible environment",
       "c": "It removes the need for a GPU",
       "d": "It automatically monitors model performance", "ans": "B", "difficulty": "medium"},
      {"text": "In CI/CD for ML, what is a common automated test to run on each code commit?",
       "a": "Full retraining of the production model",
       "b": "Unit tests, data validation checks, and model performance regression tests",
       "c": "Hyperparameter search",
       "d": "A/B test in production", "ans": "B", "difficulty": "hard"},
      {"text": "Shadow deployment in ML serving refers to:",
       "a": "Deploying a model during night hours only",
       "b": "Running a new model in parallel with production, logging its predictions without serving them to users",
       "c": "Deploying a model behind a VPN",
       "d": "Training a model on anonymised data", "ans": "B", "difficulty": "hard"},
    ],
  },
]},

{
"title": "Generative AI & Diffusion Models",
"description": "Explore the cutting edge of AI generation — GANs, VAEs, Diffusion Models, Stable Diffusion, and prompt engineering.",
"difficulty": "advanced",
"category": "Generative AI",
"lessons": [
  {
    "title": "GANs & Variational Autoencoders",
    "content": (
      "Generative models learn to produce new data samples similar to the training distribution.\n\n"
      "Variational Autoencoder (VAE):\n"
      "• Encoder: input → latent distribution (μ, σ)\n"
      "• Reparameterisation trick: z = μ + σ·ε, ε ~ N(0,1)\n"
      "• Decoder: z → reconstructed output\n"
      "• Loss = Reconstruction loss + KL divergence\n"
      "• KL divergence keeps the latent space smooth\n"
      "• Applications: image generation, anomaly detection, drug discovery\n\n"
      "Generative Adversarial Network (GAN):\n"
      "• Generator G: random noise z → fake data\n"
      "• Discriminator D: real or fake?\n"
      "• Minimax game: G tries to fool D, D tries to detect G\n"
      "• Training is unstable — mode collapse, vanishing gradients\n\n"
      "GAN variants:\n"
      "• DCGAN — uses CNNs for images\n"
      "• StyleGAN — controls image style at different scales (photorealistic faces)\n"
      "• Conditional GAN (cGAN) — generate conditioned on a class label\n"
      "• Pix2Pix — image-to-image translation\n"
      "• CycleGAN — unpaired image-to-image translation"
    ),
    "difficulty": "advanced",
    "order": 1,
    "quiz_title": "GANs & VAEs Quiz",
    "questions": [
      {"text": "In a GAN, the Generator's goal is to:",
       "a": "Classify real vs fake images",
       "b": "Produce fake data that the Discriminator cannot distinguish from real data",
       "c": "Compress images into a latent space",
       "d": "Minimise reconstruction loss", "ans": "B", "difficulty": "easy"},
      {"text": "What does the KL divergence term in a VAE's loss function encourage?",
       "a": "Better image reconstruction quality",
       "b": "The latent space distribution to remain close to a standard normal distribution",
       "c": "The decoder to produce sharper images",
       "d": "Faster training convergence", "ans": "B", "difficulty": "medium"},
      {"text": "What is mode collapse in GAN training?",
       "a": "The discriminator stops learning",
       "b": "The generator produces limited variety, outputting only a few types of samples",
       "c": "The GAN achieves perfect generation too quickly",
       "d": "The learning rate becomes too large", "ans": "B", "difficulty": "medium"},
      {"text": "CycleGAN is designed for:",
       "a": "Generating images from text prompts",
       "b": "Unpaired image-to-image translation without needing matched image pairs",
       "c": "Training on cyclical data",
       "d": "Generating sequences of video frames", "ans": "B", "difficulty": "hard"},
      {"text": "The reparameterisation trick in VAEs is used to:",
       "a": "Speed up the encoder",
       "b": "Enable backpropagation through the stochastic sampling step by expressing z as μ + σ·ε",
       "c": "Regularise the decoder weights",
       "d": "Encode discrete latent variables", "ans": "B", "difficulty": "hard"},
    ],
  },
  {
    "title": "Diffusion Models & Prompt Engineering",
    "content": (
      "Diffusion models are the current state-of-the-art for image and video generation.\n\n"
      "How diffusion models work:\n"
      "• Forward process: gradually add Gaussian noise to an image over T steps\n"
      "  x_T ≈ N(0, I)\n"
      "• Reverse process: neural network (U-Net) learns to denoise\n"
      "  p(x_{t-1} | x_t) — predict and remove noise at each step\n"
      "• Training: predict the noise added at each step (ε-prediction)\n\n"
      "Key models:\n"
      "• DDPM (Denoising Diffusion Probabilistic Models) — Ho et al. 2020\n"
      "• Stable Diffusion — latent diffusion in compressed space\n"
      "• DALL-E 3, Midjourney, Imagen — text-to-image\n"
      "• Sora — video generation\n\n"
      "Stable Diffusion components:\n"
      "• VAE encoder/decoder — compress/decompress images\n"
      "• CLIP text encoder — encode text prompts\n"
      "• U-Net — denoise in latent space\n\n"
      "Prompt Engineering:\n"
      "• Positive prompt: what you want\n"
      "• Negative prompt: what to avoid\n"
      "• CFG (Classifier-Free Guidance) scale — how closely to follow the prompt\n"
      "• LoRA — lightweight fine-tuning to add new concepts/styles"
    ),
    "difficulty": "advanced",
    "order": 2,
    "quiz_title": "Diffusion Models Quiz",
    "questions": [
      {"text": "In a diffusion model, the forward process does what to an image?",
       "a": "Generates a new image from noise",
       "b": "Gradually adds Gaussian noise until the image becomes pure noise",
       "c": "Compresses the image into a latent vector",
       "d": "Applies style transfer", "ans": "B", "difficulty": "easy"},
      {"text": "Stable Diffusion performs the diffusion process in:",
       "a": "Full pixel space", "b": "A compressed latent space produced by a VAE",
       "c": "Fourier frequency space", "d": "The attention layer of a Transformer", "ans": "B", "difficulty": "medium"},
      {"text": "What is the role of CLIP in text-to-image diffusion models?",
       "a": "To denoise the image at each timestep",
       "b": "To encode the text prompt into an embedding that guides the image generation",
       "c": "To compress the generated image",
       "d": "To score the realism of generated images", "ans": "B", "difficulty": "medium"},
      {"text": "What does CFG (Classifier-Free Guidance) scale control?",
       "a": "The number of denoising steps",
       "b": "How strongly the model adheres to the text prompt — higher values = more prompt-faithful but less diverse",
       "c": "The resolution of the generated image",
       "d": "The size of the VAE latent space", "ans": "B", "difficulty": "hard"},
      {"text": "LoRA (Low-Rank Adaptation) is used to fine-tune diffusion models by:",
       "a": "Retraining all weights on a new dataset",
       "b": "Adding small low-rank weight matrices to existing layers, dramatically reducing trainable parameters",
       "c": "Replacing the U-Net with a Transformer",
       "d": "Increasing the number of denoising timesteps", "ans": "B", "difficulty": "hard"},
    ],
  },
]},

] # end COURSES list

# ─────────────────────────────────────────────────────────────────────────────
def seed():
    total_courses = total_lessons = total_quizzes = total_questions = 0

    for c_data in COURSES:
        existing = db.query(Course).filter(Course.title == c_data["title"]).first()
        if existing:
            print(f"  [skip] '{c_data['title']}' already exists")
            continue

        course = Course(
            title=c_data["title"],
            description=c_data["description"],
            difficulty=c_data["difficulty"],
            category=c_data["category"],
        )
        db.add(course); db.commit(); db.refresh(course)
        total_courses += 1
        print(f"  [+] {c_data['difficulty'].upper():12} '{course.title}' (id={course.id})")

        for l_data in c_data["lessons"]:
            lesson = Lesson(
                course_id=course.id,
                title=l_data["title"],
                content=l_data["content"],
                difficulty=l_data["difficulty"],
                order=l_data["order"],
            )
            db.add(lesson); db.commit(); db.refresh(lesson)
            total_lessons += 1

            quiz = Quiz(lesson_id=lesson.id, title=l_data["quiz_title"])
            db.add(quiz); db.commit(); db.refresh(quiz)
            total_quizzes += 1

            for q in l_data["questions"]:
                db.add(Question(
                    quiz_id=quiz.id,
                    question_text=q["text"],
                    option_a=q["a"], option_b=q["b"],
                    option_c=q["c"], option_d=q["d"],
                    correct_answer=q["ans"],
                    difficulty=q["difficulty"],
                ))
                total_questions += 1
            db.commit()
            print(f"       |-- '{lesson.title}' -> quiz id={quiz.id}, {len(l_data['questions'])} questions")

    db.close()
    print()
    print("=" * 60)
    print(f"  Added  {total_courses} courses | {total_lessons} lessons | "
          f"{total_quizzes} quizzes | {total_questions} questions")
    print("=" * 60)
    if total_courses == 0:
        print("  (Nothing new — all courses already existed)")

if __name__ == "__main__":
    print("Seeding extended AIML curriculum...\n")
    seed()
