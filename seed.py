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
        ],
        "options": [
            "Supervised learning uses labelled data where each example has an input and an expected output and is used for classification and regression",
            "Supervised learning uses unlabelled data to find hidden patterns and clusters in the data",
            "Supervised learning only works for image recognition tasks and cannot be used for text",
            "Supervised learning does not require any training data and learns from rules written by humans"
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
        ],
        "options": [
            "Overfitting is when a model memorizes training data including noise so it fails on new data and can be prevented with regularization and cross-validation",
            "Overfitting is when a model is too simple and cannot learn the training data properly",
            "Overfitting only happens in deep learning and not in traditional machine learning models",
            "Overfitting is when a model performs poorly on both training and test data at the same time"
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
        ],
        "options": [
            "Classification predicts categories like spam or not spam while regression predicts continuous numbers like house prices",
            "Classification predicts numbers and regression predicts categories — they are the opposite of what most people think",
            "Classification and regression are both unsupervised learning techniques used for clustering data",
            "Classification is only used in deep learning while regression is only used in traditional machine learning"
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
        ],
        "options": [
            "A decision tree splits data into branches based on feature values where each leaf is a prediction and deep trees tend to overfit",
            "A decision tree is a neural network with multiple layers that learns complex patterns from data",
            "A decision tree can only be used for regression problems and not for classification",
            "A decision tree requires all features to be numerical and cannot handle categorical data"
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
        ],
        "options": [
            "Overfitting is too complex and memorizes training data while underfitting is too simple and cannot learn — the goal is the bias variance tradeoff",
            "Underfitting happens when you have too much training data and the model gets confused by the volume",
            "Overfitting and underfitting are the same problem just described from different perspectives",
            "Underfitting only happens in regression problems and overfitting only happens in classification problems"
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
        ],
        "options": [
            "Neural networks are brain-inspired models with input hidden and output layers where weights are adjusted during training for tasks like image recognition",
            "Neural networks are rule-based systems where humans manually program every decision the model makes",
            "Neural networks can only be used for image recognition and have no applications in text or audio",
            "Neural networks have no layers — they are a single mathematical function that maps inputs to outputs"
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
        ],
        "options": [
            "Deep learning needs lots of data expensive hardware and produces black box models that are hard to interpret and deploy",
            "Deep learning has no limitations and always outperforms traditional machine learning in every situation",
            "The only limitation of deep learning is that it requires a lot of data but hardware cost is never an issue",
            "Deep learning models are always easy to interpret because they use simple mathematical operations"
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
        ],
        "options": [
            "Backpropagation trains neural networks by passing error backwards from output to input and using gradient descent to adjust weights",
            "Backpropagation is a technique for collecting training data by feeding it forward through the network",
            "Backpropagation only works for classification problems and cannot be used for regression",
            "Backpropagation adjusts the architecture of the network by adding or removing layers during training"
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
        ],
        "options": [
            "Dropout randomly turns off neurons during training to prevent overfitting and force the network to learn robust features",
            "Dropout permanently removes weak neurons from the network to make it smaller and faster",
            "Dropout is applied at test time to make predictions more accurate by averaging multiple outputs",
            "Dropout increases the learning rate during training to help the model converge faster"
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
        ],
        "options": [
            "CNNs use filters for spatial data like images while RNNs have memory for sequential data like text",
            "CNNs are used for text processing and RNNs are used for image recognition — they are the opposite",
            "CNNs and RNNs are identical architectures just trained on different datasets",
            "RNNs use filters just like CNNs but apply them to time steps instead of spatial locations"
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
        ],
        "options": [
            "A BST has at most two children where left values are smaller and right values are greater giving O log n search but degrades to O n when unbalanced",
            "A binary search tree stores all values in sorted order in an array and uses binary search to find elements",
            "In a binary search tree the right subtree contains smaller values and the left subtree contains larger values",
            "A binary search tree always has O 1 search time because it uses hashing to find elements directly"
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
        ],
        "options": [
            "Stack is LIFO with push and pop used for function calls while queue is FIFO with enqueue and dequeue used for task scheduling",
            "Stack is FIFO and queue is LIFO — they follow opposite ordering principles to each other",
            "Both stack and queue follow FIFO but stack uses different method names for adding and removing",
            "Stacks are used for task scheduling and queues are used for function call management"
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
        ],
        "options": [
            "Dynamic programming breaks problems into overlapping subproblems storing results to avoid recalculation using memoization top down or tabulation bottom up",
            "Dynamic programming is another name for recursion and both terms mean exactly the same thing",
            "Dynamic programming only works for sorting problems and cannot be applied to graph or string problems",
            "Dynamic programming always uses more memory than recursion and is therefore only used as a last resort"
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
        ],
        "options": [
            "Arrays have O 1 access via index in contiguous memory while linked lists have O n access but faster insertion and deletion",
            "Linked lists are always faster than arrays for every operation because they use dynamic memory",
            "Arrays and linked lists have identical time complexity for all operations but different memory usage",
            "Arrays are faster for insertion and deletion while linked lists are faster for reading by index"
        ]
    },
    {
        "question": "What is Big O notation?",
        "domain": "DSA",
        "difficulty": "easy",
        "answer": "Big O notation describes how the time or space requirements of an algorithm grow as the input size grows. It describes the worst case scenario. Common complexities are O 1 constant O log n logarithmic O n linear O n squared quadratic and O 2 to the n exponential. It helps compare algorithms regardless of hardware.",
        "key_concepts": [
            "describes how algorithm grows",
            "worst case scenario",
            "O 1 constant",
            "O log n logarithmic",
            "O n linear",
            "O n squared quadratic",
            "compare algorithms"
        ],
        "options": [
            "Big O describes worst case growth of time or space as input grows with common complexities O 1 O log n O n and O n squared",
            "Big O notation measures the exact running time of an algorithm in milliseconds on a specific machine",
            "Big O notation only applies to sorting algorithms and cannot be used for other types of algorithms",
            "Big O always describes the best case scenario so you know how fast an algorithm can possibly run"
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
        ],
        "options": [
            "A RESTful API uses HTTP methods GET POST PUT DELETE is stateless and returns JSON making it simple and scalable",
            "A RESTful API requires a persistent connection between client and server to work correctly",
            "REST APIs can only use GET and POST methods — PUT and DELETE are not part of the REST standard",
            "RESTful APIs always return XML data and cannot return JSON format"
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
        ],
        "options": [
            "Indexing speeds up reads by allowing faster lookups but slows down writes because the index must also be updated",
            "Database indexes speed up both reads and writes equally with no tradeoffs",
            "Adding more indexes always improves database performance so you should index every column",
            "Indexes only work for primary key columns and cannot be created on other columns"
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
        ],
        "options": [
            "Caching stores frequently accessed data in a faster layer to reduce database load using tools like Redis with the main challenge being cache invalidation",
            "Caching permanently stores all data in memory so the database is never needed again",
            "Caching is only useful for write-heavy applications and has no benefit for read-heavy ones",
            "The main challenge with caching is choosing between Redis and Memcached not managing stale data"
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
        ],
        "options": [
            "SQL uses structured tables with fixed schemas for relational data while NoSQL uses flexible formats for unstructured data and scales horizontally",
            "NoSQL databases are always faster than SQL databases regardless of the use case",
            "SQL and NoSQL databases are interchangeable and the choice between them does not matter",
            "NoSQL databases support complex joins better than SQL databases which is why they are preferred"
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
        ],
        "options": [
            "Load balancing distributes requests across servers to prevent overload improve availability and redirect traffic when a server goes down",
            "Load balancing compresses all requests into a single server to process them more efficiently",
            "Load balancing only works when all servers have identical hardware and software configurations",
            "The purpose of load balancing is to reduce the number of servers needed by combining their capacity"
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
        ],
        "options": [
            "Lists are mutable with square brackets while tuples are immutable with parentheses and are faster for fixed data",
            "Lists and tuples are identical in Python — the only difference is the syntax used to create them",
            "Tuples are mutable and lists are immutable — tuples are used when you need to change the data",
            "Lists use parentheses and tuples use square brackets — the opposite of what most people think"
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
        ],
        "options": [
            "Decorators wrap functions using @ symbol to add behavior like logging authentication and route registration without modifying the original",
            "Decorators permanently change the original function by adding new lines of code directly to it",
            "Decorators can only be used for logging purposes and have no other practical applications",
            "The @ symbol in Python is only used for matrix multiplication and has nothing to do with decorators"
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
        ],
        "options": [
            "== checks value equality while is checks if two variables point to the same object in memory — use is for None checks",
            "== and is are completely identical operators in Python and can always be used interchangeably",
            "The is operator checks if two values are equal and == checks if they are the same object in memory",
            "You should always use is instead of == because it is faster and more accurate for all comparisons"
        ]
    },
    {
        "question": "What are *args and **kwargs in Python?",
        "domain": "Python",
        "difficulty": "medium",
        "answer": "args allows a function to accept any number of positional arguments collected into a tuple inside the function. kwargs allows a function to accept any number of keyword arguments collected into a dictionary inside the function. You use args when you do not know how many positional arguments will be passed and kwargs for named arguments.",
        "key_concepts": [
            "args for positional arguments",
            "kwargs for keyword arguments",
            "args collected into tuple",
            "kwargs collected into dictionary",
            "unknown number of arguments",
            "flexible function signatures"
        ],
        "options": [
            "args collects unknown positional arguments into a tuple and kwargs collects unknown keyword arguments into a dictionary",
            "args and kwargs are just naming conventions — any variable name with * or ** works the same way",
            "args collects keyword arguments and kwargs collects positional arguments — they are the opposite",
            "args and kwargs can only be used together and cannot be used independently in a function"
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
        ],
        "options": [
            "A virtual environment isolates packages per project preventing version conflicts and is created with python -m venv",
            "A virtual environment is a cloud-based Python installation that runs on remote servers",
            "Virtual environments are only needed when working with machine learning libraries not regular Python projects",
            "You only need one virtual environment for all your projects since packages are shared anyway"
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
        ],
        "options": [
            "A primary key uniquely identifies each row cannot be null has no duplicates and gets an automatic index for fast lookups",
            "A primary key is just a label for the table and does not have to be unique across rows",
            "A table can have multiple primary keys as long as each one is unique within its own column",
            "Primary keys are optional in databases and tables work fine without them"
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
        ],
        "options": [
            "A foreign key references another table's primary key creating a link enforced by the database through referential integrity",
            "A foreign key is a duplicate of the primary key stored in the same table for backup purposes",
            "Foreign keys are optional hints to the database and are not actually enforced automatically",
            "A foreign key must always reference the primary key of the same table it belongs to"
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
        ],
        "options": [
            "Normalization reduces redundancy by splitting tables and linking with foreign keys following normal forms like 1NF 2NF and 3NF",
            "Normalization combines all tables into one large table to make queries simpler and faster",
            "Database normalization is only necessary for databases with more than one million rows",
            "Normalization always makes databases faster which is why every database should be fully normalized"
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
        ],
        "options": [
            "WHERE filters rows before grouping while HAVING filters groups after GROUP BY and can use aggregate functions like COUNT and SUM",
            "WHERE and HAVING are completely interchangeable and can be used in place of each other in any query",
            "HAVING filters rows before grouping and WHERE filters groups after aggregation — they are the opposite",
            "WHERE can use aggregate functions like COUNT but HAVING cannot — that is the main difference between them"
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
        ],
        "options": [
            "A transaction groups operations as one unit where all succeed and commit or all fail and rollback following ACID properties",
            "A transaction is just another word for a single SQL query and has no special properties",
            "Transactions only apply to SELECT statements and cannot be used with INSERT UPDATE or DELETE",
            "ACID stands for Arrays Columns Indexes and Data — the four components of every database transaction"
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
        ],
        "options": [
            "Mean is the average median is the middle value and mode is most frequent — median is best when outliers exist",
            "Median is the average mean is the middle value and mode is the least frequent value in the dataset",
            "Mean median and mode always give the same result when the dataset is large enough",
            "Mode is the best measure of central tendency for all types of data including numerical data"
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
        ],
        "options": [
            "Standard deviation measures spread from the mean — low means close together high means spread out and it is the square root of variance",
            "Standard deviation measures the average value of a dataset just like the mean does",
            "A high standard deviation always means the data has errors and needs to be cleaned",
            "Standard deviation is the square of the variance not the square root"
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
        ],
        "options": [
            "Correlation means variables move together but causation means one causes the other — correlation does not imply causation",
            "Correlation and causation mean the same thing — if two variables are correlated one must cause the other",
            "Causation is always stronger than correlation and should always be preferred in data analysis",
            "In machine learning we always establish causation not just correlation before making predictions"
        ]
    },
    {
        "question": "What is a normal distribution?",
        "domain": "Statistics",
        "difficulty": "medium",
        "answer": "A normal distribution is a bell-shaped curve where most values cluster around the mean and fewer values appear as you move away from it. It is symmetric around the mean. About 68 percent of values fall within one standard deviation of the mean and 95 percent within two. Many real-world things follow a normal distribution like heights and test scores.",
        "key_concepts": [
            "bell shaped curve",
            "most values near the mean",
            "symmetric around mean",
            "68 percent within one standard deviation",
            "95 percent within two",
            "real world examples",
            "feature distributions in ML"
        ],
        "options": [
            "Normal distribution is a bell curve symmetric around the mean where 68 percent of values fall within one standard deviation",
            "A normal distribution is skewed to the right which is why it is called normal — it is the most common shape",
            "In a normal distribution exactly 50 percent of values fall within one standard deviation of the mean",
            "Normal distributions only occur in artificial datasets and are never found in real-world data"
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
        ],
        "options": [
            "Hypothesis testing uses null and alternative hypotheses and rejects the null when the p-value falls below 0.05",
            "In hypothesis testing you always start by assuming the alternative hypothesis is true and try to disprove it",
            "A p-value above 0.05 proves the alternative hypothesis is correct and the null hypothesis is wrong",
            "Hypothesis testing is only used in medical research and has no applications in machine learning or data science"
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
        ],
        "options": [
            "A process has its own memory while threads run inside a process sharing memory and can cause race conditions when accessing shared data",
            "A process and a thread are the same thing — they are just different names for the same concept",
            "Threads have their own separate memory space and cannot share data with other threads in the same process",
            "Processes are faster than threads because they are smaller and use less memory"
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
        ],
        "options": [
            "Recursion is when a function calls itself with a base case to stop it — without a base case it causes a stack overflow",
            "Recursion is when two functions call each other in a loop and is always more efficient than iteration",
            "The base case in recursion is optional — recursive functions work fine without one in most situations",
            "Recursion can only be used for mathematical problems like factorial and has no use in data structures"
        ]
    },
    {
        "question": "What is object oriented programming?",
        "domain": "Python",
        "difficulty": "easy",
        "answer": "Object oriented programming is a way of writing code by organizing it into objects that combine data and behavior. A class is a blueprint and an object is an instance of that class. The four main concepts are encapsulation which bundles data and methods together inheritance which lets a class reuse code from another class polymorphism which allows different classes to share the same interface and abstraction which hides complexity.",
        "key_concepts": [
            "objects combine data and behavior",
            "class is a blueprint",
            "object is an instance",
            "encapsulation",
            "inheritance",
            "polymorphism",
            "abstraction"
        ],
        "options": [
            "OOP organizes code into objects with a class as blueprint using encapsulation inheritance polymorphism and abstraction",
            "Object oriented programming means writing all code inside functions and never using global variables",
            "In OOP a class is an instance of an object — the class is created from the object not the other way around",
            "OOP only has three pillars — encapsulation inheritance and polymorphism — abstraction is not part of OOP"
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
        ],
        "options": [
            "Supervised uses labelled data with correct outputs while unsupervised uses unlabelled data to find patterns like clustering",
            "Supervised learning is always better than unsupervised learning and should be used whenever possible",
            "Unsupervised learning uses labelled data and supervised learning uses unlabelled data — they are the opposite",
            "Both supervised and unsupervised learning require labelled data — the difference is how the labels are used"
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
        ],
        "options": [
            "Git tracks code changes through commits lets you go back to previous versions and allows collaboration through branches",
            "Git is a programming language used specifically for writing version control systems and CI/CD pipelines",
            "GitHub and Git are the same thing — GitHub is just the command line version and Git is the website",
            "Git only works for solo developers and cannot be used when multiple people work on the same project"
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
        embedding=embedding,
        options=item["options"]
    )
    db.add(reference_answer)
    db.commit()

    print(f"Seeded: {item['question']}")