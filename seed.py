from app.db.session import SessionLocal
from app.db.models import Question, ReferenceAnswer
from app.core.embeddings import get_embedding

questions_data = [
    {
        "question": "What is supervised learning?",
        "domain": "ML",
        "answer": "Supervised learning is a type of machine learning where the model learns from labelled data. Each training example consists of input features and expected outputs called labels. The algorithm learns to map inputs to outputs. It is used for two main tasks: classification, where the output is a category such as spam detection, and regression, where the output is a continuous value such as house price prediction.",
        "key_concepts": [
            "labelled data",
            "input features",
            "output labels",
            "classification",
            "regression",
            "mapping inputs to outputs"
        ]
    },
    {
        "question": "What is overfitting and how can you prevent it?",
        "domain": "ML",
        "answer": "Overfitting happens when a model learns noise and details from the training data to the extent that it negatively impacts performance on new unseen data. The model performs well on training data but poorly on test data. Prevention techniques include regularization, using more training data, feature selection, cross-validation, early stopping for neural networks, and simplifying the model.",
        "key_concepts": [
            "noise",
            "training data",
            "unseen data",
            "generalization",
            "regularization",
            "cross-validation",
            "early stopping",
            "model complexity"
        ]
    },
    {
        "question": "What are neural networks?",
        "domain": "DL",
        "answer": "Neural networks are computational models inspired by the human brain, consisting of interconnected layers of nodes called neurons. They are organized into an input layer, one or more hidden layers, and an output layer. Each connection has a weight that is adjusted during training. Neural networks are used for both supervised and unsupervised learning and are especially powerful for complex tasks such as image recognition, natural language processing, and speech recognition.",
        "key_concepts": [
            "neurons",
            "input layer",
            "hidden layers",
            "output layer",
            "weights",
            "training",
            "image recognition",
            "natural language processing"
        ]
    },
    {
        "question": "What are the limitations of deep learning?",
        "domain": "DL",
        "answer": "Deep learning has several limitations. It is data intensive and requires large labeled datasets to perform well. It is computationally expensive requiring significant hardware and time for training. Models are often difficult to interpret giving black box predictions with no clear explanation. They are sensitive to adversarial attacks where small crafted input changes can cause wrong predictions. Overfitting can occur if the model is not regularized properly or data is scarce. Large models can also be difficult to deploy and update in production environments.",
        "key_concepts": [
            "data intensive",
            "computational cost",
            "interpretability",
            "black box",
            "adversarial attacks",
            "overfitting",
            "deployment",
            "labeled datasets"
        ]
    },
    {
        "question": "What is feature engineering?",
        "domain": "ML",
        "answer": "Feature engineering is the process of using domain knowledge to create new features or transform existing ones from raw data in order to improve model performance. It involves selecting the most relevant features, combining features, encoding categorical variables, handling missing values, and scaling numerical features. Good feature engineering can significantly improve model accuracy and reduce training time.",
        "key_concepts": [
            "domain knowledge",
            "feature creation",
            "feature transformation",
            "model performance",
            "feature selection",
            "encoding",
            "scaling",
            "raw data"
        ]
    },
    {
        "question": "What is a binary search tree?",
        "domain": "DSA",
        "answer": "A binary search tree is a tree data structure where each node has at most two children referred to as the left child and the right child. For every node, all values in the left subtree are smaller than the node value and all values in the right subtree are greater. This property makes searching, insertion and deletion efficient with an average time complexity of O(log n). However in the worst case when the tree is unbalanced it degrades to O(n).",
        "key_concepts": [
            "tree structure",
            "left subtree",
            "right subtree",
            "searching",
            "insertion",
            "deletion",
            "time complexity",
            "balanced vs unbalanced"
        ]
    },
    {
        "question": "What is the difference between a stack and a queue?",
        "domain": "DSA",
        "answer": "A stack is a linear data structure that follows the Last In First Out principle meaning the last element added is the first one removed. Operations are push to add and pop to remove. A queue is a linear data structure that follows the First In First Out principle meaning the first element added is the first one removed. Operations are enqueue to add and dequeue to remove. Stacks are used in function call management and undo operations while queues are used in task scheduling and breadth first search.",
        "key_concepts": [
            "LIFO",
            "FIFO",
            "push",
            "pop",
            "enqueue",
            "dequeue",
            "function call management",
            "task scheduling"
        ]
    },
    {
        "question": "What is dynamic programming?",
        "domain": "DSA",
        "answer": "Dynamic programming is an algorithmic technique for solving complex problems by breaking them down into simpler overlapping subproblems and storing the results of subproblems to avoid redundant computation. It has two main approaches: memoization which is top down and stores results of recursive calls, and tabulation which is bottom up and builds a table iteratively. Dynamic programming is used when a problem has optimal substructure and overlapping subproblems. Common examples include fibonacci sequence, knapsack problem and longest common subsequence.",
        "key_concepts": [
            "overlapping subproblems",
            "optimal substructure",
            "memoization",
            "tabulation",
            "top down",
            "bottom up",
            "redundant computation",
            "subproblem results"
        ]
    },
    {
        "question": "What is a RESTful API?",
        "domain": "System Design",
        "answer": "A RESTful API is an application programming interface that follows the principles of Representational State Transfer. It uses standard HTTP methods: GET to retrieve data, POST to create data, PUT to update data and DELETE to remove data. REST APIs are stateless meaning each request contains all information needed to process it. They communicate using standard formats like JSON or XML. Key principles include statelessness, client server separation, uniform interface, and cacheability. RESTful APIs are widely used because they are simple, scalable and platform independent.",
        "key_concepts": [
            "HTTP methods",
            "stateless",
            "GET POST PUT DELETE",
            "JSON",
            "client server separation",
            "uniform interface",
            "cacheability",
            "scalability"
        ]
    },
    {
        "question": "What is database indexing?",
        "domain": "System Design",
        "answer": "Database indexing is a technique used to speed up the retrieval of records from a database by creating a data structure that allows faster lookups. An index works similarly to a book index — instead of scanning every page you go directly to the relevant entry. Indexes are created on columns that are frequently searched or used in join operations. While indexes significantly improve read performance they slow down write operations such as insert update and delete because the index must also be updated. Common types include B-tree indexes, hash indexes and full text indexes.",
        "key_concepts": [
            "faster retrieval",
            "data structure",
            "B-tree",
            "read performance",
            "write performance",
            "columns",
            "join operations",
            "full text index"
        ]
    }
]

db = SessionLocal()

if db.query(Question).first():
    print("Database already seeded")
    db.close()
    exit()

for item in questions_data:
    question = Question(
        text=item["question"],
        domain=item["domain"]
    )
    db.add(question)
    db.commit()
    db.refresh(question)

    embedding = get_embedding(item["answer"])

    reference_answer = ReferenceAnswer(
        question_id=question.id,
        answer=item["answer"],
        key_concepts=item["key_concepts"],
        embedding=embedding
    )
    db.add(reference_answer)
    db.commit()

    print(f"Seeded: {item['question']}")