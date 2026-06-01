from app.db.session import SessionLocal
from app.db.models import Question, ReferenceAnswer
from app.core.embeddings import get_embedding

questions_data = [
    {
        "question": "What is supervised learning?",
        "domain": "ML",
        "difficulty": "easy",
        "answer": "Supervised learning is a type of machine learning where the model learns from labelled data. Each training example has input features and an expected output called a label. The algorithm learns to map inputs to outputs. It is used for classification tasks like spam detection and regression tasks like house price prediction.",
        "key_concepts": [
            "learns from labelled data",
            "input and output pairs",
            "classification",
            "regression",
            "predicts output",
            "training examples"
        ]
    },
    {
        "question": "What is overfitting and how can you prevent it?",
        "domain": "ML",
        "difficulty": "medium",
        "answer": "Overfitting happens when a model memorizes the training data too well including the noise so it fails on new data. It performs well on training but poorly on test data. You can prevent it using regularization cross-validation early stopping or by simplifying the model.",
        "key_concepts": [
            "memorizes training data",
            "fails on new data",
            "performs well on training",
            "poorly on test data",
            "regularization",
            "cross-validation",
            "early stopping",
            "too complex"
        ]
    },
    {
        "question": "What is the difference between classification and regression?",
        "domain": "ML",
        "difficulty": "easy",
        "answer": "Classification predicts a category or class label like spam or not spam. Regression predicts a continuous number like house price or temperature. Both are supervised learning tasks. Examples of classification algorithms are logistic regression and decision trees. Examples of regression algorithms are linear regression and random forest.",
        "key_concepts": [
            "classification predicts categories",
            "regression predicts numbers",
            "supervised learning",
            "logistic regression",
            "linear regression",
            "continuous output",
            "discrete output"
        ]
    },
    {
        "question": "What is a decision tree?",
        "domain": "ML",
        "difficulty": "easy",
        "answer": "A decision tree is a model that splits data into branches based on feature values to make predictions. Each internal node is a question about a feature, each branch is a possible answer, and each leaf is a prediction. It is easy to understand and visualize. The main problem is that deep trees tend to overfit.",
        "key_concepts": [
            "splits data into branches",
            "feature values",
            "internal nodes are questions",
            "leaves are predictions",
            "easy to visualize",
            "can overfit",
            "depth of tree"
        ]
    },
    {
        "question": "What is the difference between underfitting and overfitting?",
        "domain": "ML",
        "difficulty": "medium",
        "answer": "Overfitting is when a model is too complex and memorizes the training data so it fails on new data. Underfitting is when a model is too simple and cannot even learn the training data properly. Both give poor results on test data. The goal is to find the right balance which is called the bias variance tradeoff.",
        "key_concepts": [
            "overfitting is too complex",
            "underfitting is too simple",
            "fails on new data",
            "cannot learn training data",
            "bias variance tradeoff",
            "model complexity",
            "poor test performance"
        ]
    },

    {
        "question": "What are neural networks?",
        "domain": "DL",
        "difficulty": "easy",
        "answer": "Neural networks are models inspired by the human brain. They have layers of connected nodes called neurons — an input layer hidden layers and an output layer. Each connection has a weight that gets adjusted during training. They are used for complex tasks like image recognition and natural language processing.",
        "key_concepts": [
            "inspired by the brain",
            "layers of neurons",
            "input layer",
            "hidden layers",
            "output layer",
            "weights adjusted during training",
            "image recognition",
            "natural language processing"
        ]
    },
    {
        "question": "What are the limitations of deep learning?",
        "domain": "DL",
        "difficulty": "medium",
        "answer": "Deep learning needs a lot of labelled data to work well. It is expensive to train because it requires powerful hardware. The models are hard to interpret and you often cannot explain why they made a decision. They can also overfit if the data is limited and are difficult to deploy in production.",
        "key_concepts": [
            "needs a lot of data",
            "expensive to train",
            "hard to interpret",
            "black box",
            "can overfit",
            "hard to deploy",
            "requires powerful hardware"
        ]
    },
    {
        "question": "What is backpropagation?",
        "domain": "DL",
        "difficulty": "medium",
        "answer": "Backpropagation is the algorithm used to train neural networks. It calculates how much each weight contributed to the error and adjusts the weights to reduce that error. It works by passing the error backwards through the network from the output layer to the input layer. It uses gradient descent to update the weights.",
        "key_concepts": [
            "trains neural networks",
            "calculates error contribution",
            "adjusts weights",
            "passes error backwards",
            "gradient descent",
            "output to input",
            "reduces error"
        ]
    },
    {
        "question": "What is dropout in neural networks?",
        "domain": "DL",
        "difficulty": "medium",
        "answer": "Dropout is a regularization technique used to prevent overfitting in neural networks. During training it randomly turns off a percentage of neurons so the network cannot rely too heavily on any single neuron. This forces the network to learn more robust features. At test time all neurons are used.",
        "key_concepts": [
            "prevents overfitting",
            "randomly turns off neurons",
            "regularization technique",
            "cannot rely on single neuron",
            "learns robust features",
            "only during training",
            "all neurons used at test time"
        ]
    },
    {
        "question": "What is the difference between CNN and RNN?",
        "domain": "DL",
        "difficulty": "hard",
        "answer": "A CNN or convolutional neural network is designed for spatial data like images. It uses filters to detect patterns like edges and shapes. An RNN or recurrent neural network is designed for sequential data like text or time series. It has memory — it passes information from one step to the next. CNNs are used for image recognition and RNNs are used for language modeling.",
        "key_concepts": [
            "CNN for images",
            "RNN for sequences",
            "filters detect patterns",
            "RNN has memory",
            "spatial data",
            "sequential data",
            "image recognition",
            "language modeling"
        ]
    },

    {
        "question": "What is a binary search tree?",
        "domain": "DSA",
        "difficulty": "medium",
        "answer": "A binary search tree is a tree where each node has at most two children. All values in the left subtree are smaller than the node and all values in the right subtree are greater. This makes searching inserting and deleting efficient with average time complexity of O log n. If the tree becomes unbalanced it degrades to O n.",
        "key_concepts": [
            "at most two children",
            "left values are smaller",
            "right values are greater",
            "searching is efficient",
            "O log n",
            "unbalanced degrades to O n",
            "insert and delete"
        ]
    },
    {
        "question": "What is the difference between a stack and a queue?",
        "domain": "DSA",
        "difficulty": "easy",
        "answer": "A stack follows Last In First Out — the last item added is the first one removed. You push to add and pop to remove. A queue follows First In First Out — the first item added is the first one removed. You enqueue to add and dequeue to remove. Stacks are used for function calls and undo operations. Queues are used for task scheduling.",
        "key_concepts": [
            "last in first out",
            "first in first out",
            "push and pop",
            "enqueue and dequeue",
            "function calls",
            "undo operations",
            "task scheduling"
        ]
    },
    {
        "question": "What is dynamic programming?",
        "domain": "DSA",
        "difficulty": "hard",
        "answer": "Dynamic programming is a technique for solving problems by breaking them into smaller overlapping subproblems and storing the results to avoid repeating the same calculation. There are two approaches — memoization which is top down and stores results of recursive calls and tabulation which is bottom up and builds a table iteratively. It works when a problem has overlapping subproblems and optimal substructure.",
        "key_concepts": [
            "breaking into smaller subproblems",
            "storing results",
            "avoid repeating calculations",
            "memoization",
            "tabulation",
            "top down",
            "bottom up",
            "overlapping subproblems"
        ]
    },
    {
        "question": "What is the difference between an array and a linked list?",
        "domain": "DSA",
        "difficulty": "easy",
        "answer": "An array stores elements in contiguous memory locations so you can access any element directly using its index in O 1 time. A linked list stores elements as nodes where each node points to the next. Access is O n because you have to traverse from the start. Arrays are faster for reading and linked lists are faster for inserting and deleting in the middle.",
        "key_concepts": [
            "contiguous memory",
            "direct access by index",
            "O 1 access for arrays",
            "nodes pointing to next",
            "O n access for linked list",
            "faster insertion in linked list",
            "faster reading in array"
        ]
    },
    {
        "question": "What is Big O notation?",
        "domain": "DSA",
        "difficulty": "easy",
        "answer": "Big O notation describes how the time or space requirements of an algorithm grow as the input size grows. It describes the worst case scenario. Common complexities are O 1 which is constant, O log n which is logarithmic, O n which is linear, O n squared which is quadratic, and O 2 to the n which is exponential. It helps compare algorithms regardless of hardware.",
        "key_concepts": [
            "describes how algorithm grows",
            "worst case scenario",
            "O 1 constant",
            "O log n logarithmic",
            "O n linear",
            "O n squared quadratic",
            "compare algorithms"
        ]
    },

    {
        "question": "What is a RESTful API?",
        "domain": "System Design",
        "difficulty": "easy",
        "answer": "A RESTful API uses standard HTTP methods to let systems communicate. GET retrieves data POST creates data PUT updates data and DELETE removes data. REST APIs are stateless meaning each request contains all the information needed. They return data in JSON format and are widely used because they are simple and scalable.",
        "key_concepts": [
            "HTTP methods",
            "GET POST PUT DELETE",
            "stateless",
            "each request is independent",
            "returns JSON",
            "simple and scalable"
        ]
    },
    {
        "question": "What is database indexing?",
        "domain": "System Design",
        "difficulty": "medium",
        "answer": "Database indexing speeds up data retrieval by creating a data structure that allows faster lookups. Without an index the database scans every row. With an index it goes directly to the relevant rows. Indexes improve read performance but slow down writes because the index also needs to be updated. Common types are B-tree indexes and hash indexes.",
        "key_concepts": [
            "speeds up retrieval",
            "faster lookups",
            "scans every row without index",
            "improves read performance",
            "slows down writes",
            "B-tree index",
            "hash index"
        ]
    },
    {
        "question": "What is caching and why is it used?",
        "domain": "System Design",
        "difficulty": "easy",
        "answer": "Caching stores frequently accessed data in a faster storage layer so future requests can be served faster without hitting the database. It reduces database load and improves response time. Common examples are Redis and Memcached. The main challenge is cache invalidation — deciding when to update or remove stale data.",
        "key_concepts": [
            "stores frequently accessed data",
            "faster storage layer",
            "reduces database load",
            "improves response time",
            "Redis or Memcached",
            "cache invalidation",
            "stale data"
        ]
    },
    {
        "question": "What is the difference between SQL and NoSQL databases?",
        "domain": "System Design",
        "difficulty": "medium",
        "answer": "SQL databases store data in structured tables with fixed schemas and use SQL to query. They are good for relational data with complex joins. NoSQL databases store data in flexible formats like documents key-value pairs or graphs. They are good for unstructured data and scale horizontally more easily. Examples of SQL are PostgreSQL and MySQL. Examples of NoSQL are MongoDB and Redis.",
        "key_concepts": [
            "SQL uses structured tables",
            "fixed schema",
            "NoSQL is flexible",
            "relational data",
            "unstructured data",
            "horizontal scaling",
            "PostgreSQL MySQL",
            "MongoDB Redis"
        ]
    },
    {
        "question": "What is load balancing?",
        "domain": "System Design",
        "difficulty": "medium",
        "answer": "Load balancing distributes incoming requests across multiple servers so no single server gets overwhelmed. It improves availability and reliability. If one server goes down the load balancer redirects traffic to the remaining servers. Common algorithms are round robin where requests go to each server in turn and least connections where requests go to the server with fewest active connections.",
        "key_concepts": [
            "distributes requests across servers",
            "no single server overwhelmed",
            "improves availability",
            "server goes down redirects traffic",
            "round robin",
            "least connections",
            "reliability"
        ]
    },

    {
        "question": "What is the difference between a list and a tuple in Python?",
        "domain": "Python",
        "difficulty": "easy",
        "answer": "A list is mutable meaning you can add remove or change elements after it is created. A tuple is immutable meaning once created it cannot be changed. Lists use square brackets and tuples use parentheses. Tuples are faster and use less memory. Use a tuple when the data should not change like coordinates or RGB values.",
        "key_concepts": [
            "list is mutable",
            "tuple is immutable",
            "cannot change tuple",
            "square brackets for list",
            "parentheses for tuple",
            "tuples are faster",
            "use tuple for fixed data"
        ]
    },
    {
        "question": "What are Python decorators?",
        "domain": "Python",
        "difficulty": "medium",
        "answer": "A decorator is a function that wraps another function to add extra behavior without modifying the original function. You apply a decorator using the @ symbol above the function definition. They are used for things like logging timing authentication and route registration. In FastAPI the @app.get and @app.post decorators register functions as API routes.",
        "key_concepts": [
            "wraps another function",
            "adds extra behavior",
            "does not modify original",
            "@ symbol",
            "logging and timing",
            "authentication",
            "route registration"
        ]
    },
    {
        "question": "What is the difference between == and is in Python?",
        "domain": "Python",
        "difficulty": "easy",
        "answer": "The == operator checks if two values are equal in terms of content. The is operator checks if two variables point to the exact same object in memory. Two lists with the same content are == but not is because they are stored as different objects. Use == for comparing values and is for checking identity like checking if something is None.",
        "key_concepts": [
            "== checks value equality",
            "is checks same object in memory",
            "same content but different objects",
            "use is for None check",
            "identity vs equality",
            "different memory locations"
        ]
    },
    {
        "question": "What are *args and **kwargs in Python?",
        "domain": "Python",
        "difficulty": "medium",
        "answer": "args allows a function to accept any number of positional arguments. They are collected into a tuple inside the function. kwargs allows a function to accept any number of keyword arguments. They are collected into a dictionary inside the function. You use args when you do not know how many positional arguments will be passed and kwargs for named arguments.",
        "key_concepts": [
            "args for positional arguments",
            "kwargs for keyword arguments",
            "args collected into tuple",
            "kwargs collected into dictionary",
            "unknown number of arguments",
            "flexible function signatures"
        ]
    },
    {
        "question": "What is a Python virtual environment?",
        "domain": "Python",
        "difficulty": "easy",
        "answer": "A virtual environment is an isolated Python installation for a specific project. It has its own set of packages separate from the global Python installation. This prevents version conflicts between different projects. You create one with python -m venv and activate it with venv Scripts activate on Windows. Every project should have its own virtual environment.",
        "key_concepts": [
            "isolated Python installation",
            "separate packages per project",
            "prevents version conflicts",
            "python -m venv to create",
            "activate before working",
            "independent from global Python"
        ]
    },

    {
        "question": "What is a primary key in a database?",
        "domain": "Databases",
        "difficulty": "easy",
        "answer": "A primary key is a column or set of columns that uniquely identifies each row in a table. No two rows can have the same primary key value and it cannot be null. It is used to find update or delete specific rows. Most databases automatically create an index on the primary key to make lookups faster.",
        "key_concepts": [
            "uniquely identifies each row",
            "cannot be null",
            "no duplicate values",
            "used to find specific rows",
            "index created automatically",
            "one per table"
        ]
    },
    {
        "question": "What is a foreign key?",
        "domain": "Databases",
        "difficulty": "easy",
        "answer": "A foreign key is a column in one table that references the primary key of another table. It creates a link between two tables. The database enforces this link — you cannot insert a foreign key value that does not exist in the referenced table. This is called referential integrity and it prevents orphaned data.",
        "key_concepts": [
            "references primary key of another table",
            "creates a link between tables",
            "database enforces the link",
            "cannot insert non-existent value",
            "referential integrity",
            "prevents orphaned data"
        ]
    },
    {
        "question": "What is database normalization?",
        "domain": "Databases",
        "difficulty": "medium",
        "answer": "Normalization is the process of organizing a database to reduce data redundancy and improve data integrity. It involves splitting large tables into smaller related tables and using foreign keys to link them. The main normal forms are 1NF 2NF and 3NF each with stricter rules. The goal is to store each piece of data in only one place.",
        "key_concepts": [
            "reduces data redundancy",
            "improves data integrity",
            "splitting tables",
            "foreign keys to link",
            "normal forms",
            "store data in one place",
            "1NF 2NF 3NF"
        ]
    },
    {
        "question": "What is the difference between WHERE and HAVING in SQL?",
        "domain": "Databases",
        "difficulty": "medium",
        "answer": "WHERE filters rows before any grouping happens. HAVING filters groups after a GROUP BY has been applied. You use WHERE to filter individual rows based on column values. You use HAVING to filter groups based on aggregate functions like COUNT SUM or AVG. WHERE cannot use aggregate functions but HAVING can.",
        "key_concepts": [
            "WHERE filters rows before grouping",
            "HAVING filters after GROUP BY",
            "WHERE on individual rows",
            "HAVING on groups",
            "aggregate functions",
            "COUNT SUM AVG",
            "WHERE cannot use aggregates"
        ]
    },
    {
        "question": "What is a database transaction?",
        "domain": "Databases",
        "difficulty": "medium",
        "answer": "A transaction is a group of database operations that are treated as a single unit. Either all operations succeed and are committed or if any operation fails the entire transaction is rolled back. Transactions follow ACID properties — Atomicity Consistency Isolation and Durability. A common example is a bank transfer where both the debit and credit must succeed together.",
        "key_concepts": [
            "group of operations as one unit",
            "all succeed or all fail",
            "commit or rollback",
            "ACID properties",
            "atomicity",
            "consistency",
            "isolation",
            "durability"
        ]
    },

    {
        "question": "What is the difference between mean median and mode?",
        "domain": "Statistics",
        "difficulty": "easy",
        "answer": "Mean is the average — you add all values and divide by the count. Median is the middle value when data is sorted. Mode is the most frequently occurring value. Mean is sensitive to outliers. Median is better when there are outliers because it is not affected by extreme values. Mode is used for categorical data.",
        "key_concepts": [
            "mean is the average",
            "median is the middle value",
            "mode is most frequent",
            "mean sensitive to outliers",
            "median not affected by outliers",
            "mode for categorical data",
            "sorted data for median"
        ]
    },
    {
        "question": "What is standard deviation?",
        "domain": "Statistics",
        "difficulty": "easy",
        "answer": "Standard deviation measures how spread out the values in a dataset are from the mean. A low standard deviation means values are close to the mean. A high standard deviation means values are spread out widely. It is the square root of the variance. In machine learning it is used to understand the distribution of features and to normalize data.",
        "key_concepts": [
            "measures spread from mean",
            "low means values close to mean",
            "high means values spread out",
            "square root of variance",
            "understand distribution",
            "normalize data",
            "variance"
        ]
    },
    {
        "question": "What is the difference between correlation and causation?",
        "domain": "Statistics",
        "difficulty": "medium",
        "answer": "Correlation means two variables tend to move together — when one goes up the other goes up or down. Causation means one variable directly causes the change in another. Correlation does not imply causation. For example ice cream sales and drowning rates are correlated because both increase in summer but ice cream does not cause drowning. In ML we often find correlations but cannot always claim causation.",
        "key_concepts": [
            "correlation means variables move together",
            "causation means one causes the other",
            "correlation does not imply causation",
            "confounding variables",
            "example ice cream and drowning",
            "ML finds correlations",
            "cannot always claim causation"
        ]
    },
    {
        "question": "What is a normal distribution?",
        "domain": "Statistics",
        "difficulty": "medium",
        "answer": "A normal distribution is a bell-shaped curve where most values cluster around the mean and fewer values appear as you move away from it. It is symmetric around the mean. About 68 percent of values fall within one standard deviation of the mean and 95 percent within two. Many real-world things follow a normal distribution like heights and test scores. It is important in ML for understanding feature distributions.",
        "key_concepts": [
            "bell shaped curve",
            "most values near the mean",
            "symmetric around mean",
            "68 percent within one standard deviation",
            "95 percent within two",
            "real world examples",
            "feature distributions in ML"
        ]
    },
    {
        "question": "What is hypothesis testing?",
        "domain": "Statistics",
        "difficulty": "hard",
        "answer": "Hypothesis testing is a method to decide whether there is enough evidence to support a claim about data. You start with a null hypothesis which says there is no effect and an alternative hypothesis which says there is an effect. You calculate a p-value which is the probability of seeing your results if the null hypothesis is true. If the p-value is below a threshold like 0.05 you reject the null hypothesis.",
        "key_concepts": [
            "null hypothesis no effect",
            "alternative hypothesis there is effect",
            "p-value",
            "probability of results under null",
            "reject null if p below threshold",
            "0.05 significance level",
            "statistical significance"
        ]
    },

    {
        "question": "What is the difference between a process and a thread?",
        "domain": "System Design",
        "difficulty": "medium",
        "answer": "A process is an independent program running in its own memory space. A thread is a smaller unit of execution that runs inside a process and shares the same memory. Multiple threads in the same process can run at the same time and share data easily but they can cause problems if they access the same data simultaneously which is called a race condition.",
        "key_concepts": [
            "process is independent program",
            "thread runs inside a process",
            "threads share memory",
            "multiple threads run simultaneously",
            "race condition",
            "shared data problems",
            "lightweight than process"
        ]
    },
    {
        "question": "What is recursion?",
        "domain": "DSA",
        "difficulty": "easy",
        "answer": "Recursion is when a function calls itself to solve a smaller version of the same problem. Every recursive function needs a base case which is the condition that stops the recursion. Without a base case the function calls itself forever and causes a stack overflow. Common examples are calculating factorial and traversing a tree.",
        "key_concepts": [
            "function calls itself",
            "smaller version of same problem",
            "base case stops recursion",
            "without base case infinite loop",
            "stack overflow",
            "factorial",
            "tree traversal"
        ]
    },
    {
        "question": "What is object oriented programming?",
        "domain": "Python",
        "difficulty": "easy",
        "answer": "Object oriented programming is a way of writing code by organizing it into objects that combine data and behavior. A class is a blueprint and an object is an instance of that class. The four main concepts are encapsulation which bundles data and methods together, inheritance which lets a class reuse code from another class, polymorphism which allows different classes to share the same interface, and abstraction which hides complexity.",
        "key_concepts": [
            "objects combine data and behavior",
            "class is a blueprint",
            "object is an instance",
            "encapsulation",
            "inheritance",
            "polymorphism",
            "abstraction"
        ]
    },
    {
        "question": "What is the difference between supervised and unsupervised learning?",
        "domain": "ML",
        "difficulty": "easy",
        "answer": "Supervised learning uses labelled data — the training examples have both inputs and correct outputs. The model learns to predict the output from the input. Unsupervised learning uses unlabelled data — there are no correct outputs. The model tries to find patterns or structure in the data on its own. Examples of unsupervised learning are clustering and dimensionality reduction.",
        "key_concepts": [
            "supervised uses labelled data",
            "unsupervised uses unlabelled data",
            "supervised has correct outputs",
            "unsupervised finds patterns",
            "clustering",
            "dimensionality reduction",
            "no labels in unsupervised"
        ]
    },
    {
        "question": "What is Git and why is it used?",
        "domain": "Python",
        "difficulty": "easy",
        "answer": "Git is a version control system that tracks changes to your code over time. It lets you save snapshots of your code called commits so you can go back to any previous version. It allows multiple developers to work on the same codebase without overwriting each other's work using branches. GitHub is a platform for hosting Git repositories online.",
        "key_concepts": [
            "tracks changes to code",
            "saves snapshots called commits",
            "go back to previous version",
            "multiple developers can collaborate",
            "branches",
            "GitHub for hosting",
            "version control"
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
        domain=item["domain"],
        difficulty=item["difficulty"]
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