# Complete Project Documentation — Every Line Explained
# AI-Powered Interview Answer Evaluator
# Built by Moiz Nisar

---

## Table of Contents

1. Project Overview
2. Tools and Technologies — What, Why, and Why Not Alternatives
3. Project Setup — Every Command Explained
4. `app/db/session.py` — Every Line Explained
5. `app/db/models.py` — Every Line Explained
6. `alembic/env.py` — Every Change Explained
7. `app/core/embeddings.py` — Every Line Explained
8. `app/core/similarity.py` — Every Line Explained
9. `seed.py` — Every Line Explained
10. `app/schemas/evaluation.py` — Every Line Explained
11. `app/main.py` — Every Line Explained
12. `app/core/rag.py` — Every Line Explained
13. `app/api/routes/evaluate.py` — Every Line Explained
14. `app/api/routes/questions.py` — Every Line Explained
15. `index.html` — Every Section Explained
16. Database Design — Every Decision Explained
17. The ML Pipeline — How It All Connects
18. The RAG Pipeline — How It All Connects
19. Every Error We Faced and How We Fixed It
20. Interview Questions — What If Scenarios
21. Interview Questions — Why Not This Instead
22. How to Start the Project Every Time

---

## 1. Project Overview

### What We Built

An AI-Powered Interview Answer Evaluation System. When a user submits a technical interview answer the system:

1. Converts the answer into a vector embedding using MiniLM
2. Searches PostgreSQL + pgvector for the closest reference answer
3. Computes a weighted similarity score combining semantic similarity and concept coverage
4. Detects which key concepts were covered and which were missed
5. Sends everything to LLaMA 3 via Groq API to generate improvement suggestions and a professional improved answer
6. Saves the full evaluation to the database for progress tracking
7. Returns everything as a clean JSON response

### What Problem It Solves

When someone prepares for technical interviews they write or speak answers but have no way to know:
- How correct their answer is compared to an ideal answer
- What key concepts they missed
- How to specifically improve their answer
- What a professional version of their answer looks like

This system solves all four problems automatically using real ML, not just keyword matching.

### Why This Project Is Strong for a Portfolio

- Combines real ML (embeddings, cosine similarity, vector search) with a production-grade API
- Implements RAG architecture manually without LangChain — shows deep understanding
- Uses pgvector for vector storage — a real production skill
- Shows proper database design with foreign keys, migrations, and proper data types
- Demonstrates full AI system design thinking
- Every technical decision can be explained and defended in an interview

---

## 2. Tools and Technologies — What, Why, and Why Not Alternatives

### Python
**What it is:** The programming language used for everything in this project.
**Why we used it:** Python is the standard language for ML and AI. All major ML libraries are Python-first. The ecosystem is unmatched.
**Why not JavaScript/Node.js:** JavaScript has weak ML support. Python dominates this space entirely.
**Why not Java:** Java has verbose syntax and a weaker ML ecosystem for this type of project.

---

### FastAPI
**What it is:** A modern Python web framework for building REST APIs.
**Why we used it:**
- Auto-generates Swagger UI documentation with zero extra work
- Built-in Pydantic integration for automatic request/response validation
- Async support for handling multiple simultaneous requests efficiently
- Fastest Python web framework by benchmarks

**Why not Flask:** Flask requires manual setup for everything FastAPI provides automatically. No built-in validation, no auto-generated docs, no async by default.

**Why not Django:** Django is a full-stack web framework designed for web applications with templates. It is overkill for a pure REST API. FastAPI is purpose-built for APIs.

---

### PostgreSQL
**What it is:** A powerful open-source relational database.
**Why we used it:** Industry standard, supports pgvector extension, handles relational data naturally, free and open source.
**Why not MySQL:** MySQL does not have a mature pgvector equivalent.
**Why not SQLite:** File-based, no pgvector support, can not handle concurrent requests well.
**Why not MongoDB:** NoSQL. Our data is relational. MongoDB does not support pgvector.

---

### pgvector
**What it is:** A PostgreSQL extension adding a VECTOR data type and similarity search.
**Why we used it:** Stores 384-dimensional embeddings natively, enables cosine distance search with the <=> operator, keeps vector and relational data in one database, free.
**Why not Pinecone:** Separate paid service, unnecessary for our scale (hundreds of questions). pgvector gives the same capability for free inside PostgreSQL.
**Why not Chroma or Weaviate:** Same reason. Separate infrastructure for no benefit at this scale.

---

### SQLAlchemy + Alembic
**What SQLAlchemy is:** An ORM that translates between Python objects and database tables.
**What Alembic is:** A database migration tool that tracks and applies schema changes.
**Why SQLAlchemy:** Define tables as Python classes, query using Python, type-safe, industry standard.
**Why Alembic:** Every schema change is versioned. Changes can be applied or reversed. Like Git for your database.
**Why not raw SQL:** Messy, hard to maintain, vulnerable to SQL injection.

---

### sentence-transformers (MiniLM)
**What it is:** A Python library providing pre-trained models for generating sentence embeddings. We use all-MiniLM-L6-v2.
**Why MiniLM:** 384-dimensional embeddings, 90MB model that runs on CPU, excellent semantic similarity performance, completely free, no API costs.
**Why not OpenAI embeddings:** Costs money per API call. Development testing generates hundreds of calls.
**Why not Word2Vec:** Word-level embeddings. We need sentence-level embeddings for comparing full answers.

---

### scikit-learn
**What it is:** A Python ML library. We use exactly one function from it — cosine_similarity.
**Why:** Reliable tested implementation in one line of code.

---

### Groq API with LLaMA 3
**What it is:** An AI inference service running LLaMA 3 at high speed.
**Why:** Completely free tier, sub-second inference, strong model, simple API.
**Why not OpenAI:** Costs money per token. Development testing accumulates costs quickly.
**Why not local LLM:** Requires 8-16GB RAM and is slow without a GPU.

---

### Docker
**What it is:** A platform that runs software in isolated containers.
**Why:** pgvector could not be installed on local PostgreSQL 18 on Windows. Docker's pre-built pgvector image works immediately with one command.
**Why not install locally:** Incompatibility with our PostgreSQL 18 on Windows.

---

## 3. Project Setup — Every Command Explained

### Creating the Virtual Environment

```bash
python -m venv venv
```
`python -m venv` runs Python's built-in venv module.
`venv` is the folder name for the virtual environment.
Creates a private Python installation just for this project.

```bash
venv\Scripts\activate
```
Activates the virtual environment. After this, pip installs go into the project's private environment, not globally. You see `(venv)` in the terminal when it's active.

---

### Installing Dependencies

```bash
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary pgvector sentence-transformers scikit-learn python-dotenv groq
```

Every package:
- `fastapi` — the API framework
- `uvicorn` — the server that runs FastAPI (FastAPI is the car body, uvicorn is the engine)
- `sqlalchemy` — ORM translating Python to PostgreSQL
- `alembic` — database migration tool
- `psycopg2-binary` — the actual PostgreSQL driver (SQLAlchemy needs this but you never touch it directly — it is the USB cable)
- `pgvector` — teaches SQLAlchemy to understand Vector column types
- `sentence-transformers` — MiniLM embedding model
- `scikit-learn` — cosine_similarity function
- `python-dotenv` — reads .env file
- `groq` — Groq API client

```bash
pip freeze > requirements.txt
```
`pip freeze` lists every installed package with exact version.
`> requirements.txt` writes that list to the file.
Anyone who clones the project runs `pip install -r requirements.txt` to get identical versions.

---

### Starting Docker Container

```bash
docker run --name pgvector-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=interview_evaluator -p 5432:5432 -d pgvector/pgvector:pg16
```

Every part:
- `docker run` — create and start a new container
- `--name pgvector-db` — name this container so we can reference it by name
- `-e POSTGRES_PASSWORD=postgres` — set environment variable inside container: the PostgreSQL password
- `-e POSTGRES_DB=interview_evaluator` — automatically create this database when container starts
- `-p 5432:5432` — map Windows port 5432 to container port 5432. Format is host:container. This is why Python can connect to localhost:5432 and reach Docker PostgreSQL
- `-d` — run in background (detached). Without this the container output fills your terminal
- `pgvector/pgvector:pg16` — the Docker image. Comes with PostgreSQL 16 and pgvector pre-installed

---

### Initializing Alembic

```bash
alembic init alembic
```
Creates the alembic/ folder, env.py, script.py.mako, and alembic.ini.

---

### Running Migrations

```bash
alembic revision --autogenerate -m "create initial tables"
```
`--autogenerate` compares your SQLAlchemy models against the actual database and generates the migration file automatically.
`-m` sets the description (like a Git commit message).
Creates a file in alembic/versions/ with upgrade() and downgrade() functions.

```bash
alembic upgrade head
```
Applies all pending migrations. `head` means up to the most recent.
After this, actual tables exist in PostgreSQL.

---

### Running the API

```bash
uvicorn app.main:app --reload
```
- `app.main` — go to the app/ folder, find main.py
- `:app` — use the variable named `app` inside main.py
- `--reload` — automatically restart when you save any Python file

---

## 4. `app/db/session.py` — Every Line Explained

```python
from dotenv import load_dotenv
```
Import `load_dotenv` from python-dotenv. This function reads a .env file and loads its key-value pairs into the OS environment variables.

```python
from sqlalchemy import create_engine
```
Import `create_engine`. Creates the actual database connection — everything flows through this engine.

```python
from sqlalchemy.orm import sessionmaker, declarative_base
```
`sessionmaker` — a factory that creates database sessions (conversations with the database).
`declarative_base` — creates the Base class that all table models inherit from.

```python
import os
```
Python's built-in os module. We use it to read environment variables.

```python
load_dotenv()
```
Read the .env file and load DATABASE_URL, SECRET_KEY, GROQ_API_KEY into OS environment variables. Without this, os.getenv() finds nothing.

```python
DATABASE_URL = os.getenv("DATABASE_URL")
```
`os.getenv("DATABASE_URL")` searches the OS environment variables for the key "DATABASE_URL" and returns its value.

"DATABASE_URL" is in quotes because it is a string key you are looking up — like a dictionary key. The result is stored in the variable DATABASE_URL (no quotes) for use later.

After this line, DATABASE_URL holds:
`"postgresql://postgres:postgres@localhost:5432/interview_evaluator"`

Breaking down that URL:
- `postgresql://` — database driver
- `postgres` — username
- `:postgres` — password
- `@localhost` — host (Docker maps port 5432 to your machine)
- `:5432` — port
- `/interview_evaluator` — database name

```python
engine = create_engine(DATABASE_URL)
```
Creates the SQLAlchemy engine — the actual connection to PostgreSQL. DATABASE_URL is passed without quotes because it is a variable holding the actual URL string, not the text "DATABASE_URL". The engine is the phone line between Python and the database.

```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```
Creates a session factory called SessionLocal. Calling SessionLocal() creates a new database session.

`autocommit=False` — changes are NOT saved automatically. You must call db.commit() explicitly. This gives control — make multiple changes and commit them together, or roll back if something fails.
`autoflush=False` — queries are NOT sent automatically. You control when they run.
`bind=engine` — sessions created by this factory use the engine above.

```python
Base = declarative_base()
```
Creates the Base class. Every model inherits from Base. Inheriting from Base tells SQLAlchemy this class represents a database table. Base.metadata contains the complete registry of all your tables — Alembic reads this to detect changes.

```python
def get_db():
```
A FastAPI dependency function. FastAPI calls this automatically before each route that needs a database session.

```python
    db = SessionLocal()
```
Create a new session. Opens a connection to PostgreSQL. Ready for queries.

```python
    try:
```
Start a try block. Normal execution happens here.

```python
        yield db
```
`yield` pauses the function and passes `db` to the route. Unlike `return` which stops completely, `yield` waits. FastAPI runs the route with this session. When the route finishes, FastAPI resumes get_db from after the yield.

```python
    finally:
```
`finally` runs NO MATTER WHAT — whether the route succeeded or crashed. This guarantees cleanup.

```python
        db.close()
```
Close the session. Return the connection to the pool. Without this, connections accumulate and the database eventually runs out of available connections.

---

## 5. `app/db/models.py` — Every Line Explained

```python
from app.db.session import Base
```
Import the Base class from session.py. All models inherit from this same Base instance so they are all registered in Base.metadata.

```python
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float, DateTime, func
```
Import column types and utilities:
- `Column` — defines a column
- `Integer` — whole numbers
- `String` — variable length text
- `ForeignKey` — links to another table's column
- `JSON` — stores Python lists/dicts as JSON
- `Float` — decimal numbers
- `DateTime` — date and time
- `func` — SQL functions (we use func.now() for automatic timestamps)

```python
from pgvector.sqlalchemy import Vector
```
Import the Vector type from pgvector. Adds the vector column type to SQLAlchemy. Without pgvector installed, this import fails.

---

### The Question Model

```python
class Question(Base):
```
Python class inheriting from Base. SQLAlchemy knows this represents a database table.

```python
    __tablename__ = "questions"
```
The actual PostgreSQL table name. Must be a string. Convention is lowercase with underscores.

```python
    id = Column(Integer, primary_key=True)
```
The id column. Integer stores whole numbers. `primary_key=True` makes this the unique identifier. PostgreSQL auto-increments it (1, 2, 3...) — you never set it manually.

```python
    text = Column(String, nullable=False)
```
The question text column. `nullable=False` means this column cannot be empty. Every row must have a value. PostgreSQL enforces this — trying to insert a row without text raises an error.

```python
    domain = Column(String, nullable=False)
```
The domain column storing "ML", "DL", "DSA", or "System Design". Required for every question.

---

### The ReferenceAnswer Model

```python
class ReferenceAnswer(Base):
    __tablename__ = "reference_answers"
    id = Column(Integer, primary_key=True)
```
Same pattern — inherits from Base, defines table name, has auto-incrementing primary key.

```python
    question_id = Column(Integer, ForeignKey("questions.id"))
```
Foreign key column. Stores the id of the related question. `ForeignKey("questions.id")` tells PostgreSQL: this value must exist in the id column of the questions table. PostgreSQL enforces this — you cannot insert a reference_answer pointing to a non-existent question.

```python
    answer = Column(String, nullable=False)
```
The full reference answer text. Required.

```python
    key_concepts = Column(JSON, nullable=False)
```
Stores a Python list as JSON. Example stored value: `["generalization", "noise", "training data"]`. JSON type handles list-to-database-to-list conversion automatically.

```python
    embedding = Column(Vector(384), nullable=False)
```
The pgvector column. Stores 384 floating point numbers representing the semantic meaning of the answer. The 384 must match MiniLM's output dimension exactly. Required because similarity search is impossible without it.

---

### The Evaluation Model

```python
class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True)
```

```python
    question_id = Column(Integer, ForeignKey("questions.id"))
```
Links this evaluation to a question. Enables GET /history/{question_id} — fetching all evaluations for one question.

```python
    user_answer = Column(String, nullable=False)
```
What the user actually submitted. Stored so users can see their past answers when reviewing history.

```python
    score = Column(Float, nullable=False)
```
The final weighted score. Float because scores have decimals like 87.12 or 43.06.

```python
    covered_concepts = Column(JSON, nullable=False)
    missing_concepts = Column(JSON, nullable=False)
```
Lists of concepts stored as JSON arrays.

```python
    suggestions = Column(String, nullable=False)
    improved_answer = Column(String, nullable=False)
```
Long text strings from the LLM. Can be multiple paragraphs.

```python
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
```
`DateTime(timezone=True)` — stores timestamp with timezone.
`server_default=func.now()` — PostgreSQL sets this automatically when a row is inserted. Using server_default means PostgreSQL handles it, not Python code. More reliable across different timezones and server configurations.
`nullable=False` — always required, but server_default ensures it is always set.

---

## 6. `alembic/env.py` — Every Change Explained

### Change 1 — Load Database URL

```python
config = context.config  # already existed

from dotenv import load_dotenv
import os

load_dotenv()
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
```

`config = context.config` was already there. config is the Alembic configuration object.

We added the three lines below it.

`load_dotenv()` loads the .env file.

`config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))` overrides the sqlalchemy.url setting from alembic.ini with the value from .env. This means the database URL lives in one place (.env) and both SQLAlchemy and Alembic use the same value. The password is never hardcoded in tracked files.

### Change 2 — Point to Your Models

Original:
```python
target_metadata = None
```

Changed to:
```python
from app.db.models import Base
target_metadata = Base.metadata
```

`Base.metadata` is a SQLAlchemy object containing the complete definition of every table that inherited from Base — Question, ReferenceAnswer, Evaluation.

`target_metadata = None` means Alembic is blind — it cannot see any tables and generates empty migrations.

`target_metadata = Base.metadata` means Alembic can see all three tables and generates accurate migrations by comparing them against the actual database.

---

## 7. `app/core/embeddings.py` — Every Line Explained

```python
from sentence_transformers import SentenceTransformer
```
Import the SentenceTransformer class that provides access to pre-trained embedding models.

```python
model = SentenceTransformer('all-MiniLM-L6-v2')
```
Load the MiniLM model at MODULE LEVEL — outside any function.

This runs once when Python first imports this file. The 90MB model downloads from HuggingFace on first run and caches permanently. Every subsequent run loads from cache in seconds.

Why outside a function: if inside get_embedding(), the model reloads on every API request. Loading takes 2-3 seconds. That is catastrophically slow for an API. Module-level loading means the model is always ready in memory.

```python
def get_embedding(text):
```
A function taking one string parameter. Called when seeding the database and when users submit answers.

```python
    return model.encode(text).tolist()
```
Two operations chained:

`model.encode(text)` — runs the text through MiniLM's tokenizer and 6 transformer layers. Outputs a numpy array of 384 floating point numbers. Similar sentences produce similar arrays. The numbers capture semantic meaning.

`.tolist()` — converts the numpy array to a plain Python list. pgvector expects a Python list when storing. Numpy arrays look similar but are a different type that PostgreSQL's driver does not understand. `.tolist()` converts `numpy.array([0.23, -0.81, ...])` to `[0.23, -0.81, ...]`.

---

## 8. `app/core/similarity.py` — Every Line Explained

```python
from sklearn.metrics.pairwise import cosine_similarity
```
Import cosine_similarity from scikit-learn's pairwise metrics. Measures the angle between two vectors.

```python
def compute_similarity(embedding1, embedding2):
```
Takes two embeddings — in your project always the reference embedding and user embedding.

```python
    score = cosine_similarity([embedding1], [embedding2])[0][0]
```
Four operations:

`[embedding1]` and `[embedding2]` — wrapping in square brackets creates 2D arrays. scikit-learn expects 2D arrays because it is designed for multiple pairs. Wrapping in brackets satisfies this for one pair.

`cosine_similarity([embedding1], [embedding2])` — computes similarity. Returns a nested array like `[[0.8712]]`.

`[0]` — gets the first row: `[0.8712]`
`[0]` again — gets the first element: `0.8712`

Result: a plain numpy float64.

```python
    return round(float(score) * 100, 2)
```
Three operations:

`float(score)` — converts numpy float64 to a plain Python float. CRITICAL. Without this, PostgreSQL raises an error when storing the score because numpy's float64 is not recognized as a valid PostgreSQL numeric type.

`* 100` — converts 0-1 similarity range to 0-100 scale.

`round(..., 2)` — rounds to 2 decimal places. 87.1234567 becomes 87.12.

---

## 9. `seed.py` — Every Line Explained

```python
from app.db.session import SessionLocal
```
Import the session factory to create database sessions.

```python
from app.db.models import Question, ReferenceAnswer
```
Import models to create row objects.

```python
from app.core.embeddings import get_embedding
```
Import embedding function to generate vectors for reference answers.

```python
questions_data = [...]
```
A list of dictionaries. Each dictionary is one question with its reference answer and key concepts. This is the knowledge base the evaluation system compares against.

```python
db = SessionLocal()
```
Create a database session. Opens a connection to PostgreSQL.

```python
if db.query(Question).first():
```
`db.query(Question)` creates a SELECT query on the questions table.
`.first()` executes it and returns the first row or None if empty.

If any question exists, the condition is True — database already seeded.

```python
    print("Database already seeded")
    db.close()
    exit()
```
If already seeded: print message, close the session (important — always close what you open), exit the script. Prevents duplicate data if run twice.

```python
for item in questions_data:
```
Loop through every dictionary. Each iteration, `item` holds one dictionary:
```python
{
    "question": "What is overfitting?",
    "domain": "ML",
    "answer": "Overfitting happens when...",
    "key_concepts": ["noise", "training data", ...]
}
```

```python
    question = Question(
        text=item["question"],
        domain=item["domain"]
    )
```
Create a Question object. Not saved yet — only in Python memory.

`item["question"]` accesses the "question" key from the current dictionary. `item["domain"]` accesses "domain".

`text=item["question"]` means set the text column to this value. Column name on left, value on right.

```python
    db.add(question)
```
Tell SQLAlchemy to track this object. Still not in database — queued.

```python
    db.commit()
```
Execute the INSERT. Question row physically written to PostgreSQL. PostgreSQL assigns an auto-incremented id.

```python
    db.refresh(question)
```
Fetch the latest data for this object from PostgreSQL. After commit, PostgreSQL assigned an id but the Python object does not automatically know it. db.refresh() gets the id.

CRITICAL: The next step needs question.id. Without refresh, question.id is None and the foreign key fails.

```python
    embedding = get_embedding(item["answer"])
```
Call get_embedding with the reference answer text. Returns a list of 384 numbers.

`item["answer"]` accesses the "answer" key — the reference answer text string.

```python
    reference_answer = ReferenceAnswer(
        question_id=question.id,
        answer=item["answer"],
        key_concepts=item["key_concepts"],
        embedding=embedding
    )
```
Create a ReferenceAnswer object:
- `question_id=question.id` — link to the question we just saved. Works because db.refresh() gave us the real id
- `answer=item["answer"]` — the reference text
- `key_concepts=item["key_concepts"]` — the list, stored as JSON
- `embedding=embedding` — the 384-dimensional vector

```python
    db.add(reference_answer)
    db.commit()
```
Queue and save to PostgreSQL.

```python
    print(f"Seeded: {item['question']}")
```
f-string progress output. `{item['question']}` is replaced with the actual question text.

```python
db.close()
print("Seeding complete!")
```
Close the session and confirm completion.

---

## 10. `app/schemas/evaluation.py` — Every Line Explained

```python
from pydantic import BaseModel
```
Import BaseModel. All schema classes inherit from this to get automatic validation and JSON serialization.

```python
from datetime import datetime
```
Import datetime for type-hinting the created_at field in HistoryResponse.

```python
class EvaluationRequest(BaseModel):
```
Defines what a user MUST send to POST /evaluate. Inheriting from BaseModel means FastAPI validates every incoming request against this.

```python
    question: str
    user_answer: str
```
Two required string fields. If the user sends a request without either field, or sends the wrong type, FastAPI automatically returns a 422 Validation Error before your route function runs. You write zero validation code.

```python
class EvaluationResponse(BaseModel):
    question_id: int
    score: float
    covered_concepts: list
    missing_concepts: list
    suggestions: str
    improved_answer: str
```
Defines what POST /evaluate returns. FastAPI validates your return value against this before sending. Also generates the response documentation in Swagger UI automatically.

```python
class QuestionResponse(BaseModel):
    id: int
    text: str
    domain: str
```
Shape of each question from GET /questions. Maps directly to Question model columns.

```python
class HistoryResponse(BaseModel):
    id: int
    user_answer: str
    score: float
    covered_concepts: list
    missing_concepts: list
    created_at: datetime
```
Shape of each evaluation from GET /history/{question_id}. Includes created_at as datetime so users see when each attempt was made.

---

## 11. `app/main.py` — Every Line Explained

```python
from fastapi import FastAPI
```
Import FastAPI class.

```python
from fastapi.middleware.cors import CORSMiddleware
```
Import CORSMiddleware. CORS (Cross-Origin Resource Sharing) is a browser security feature blocking requests from one origin to another. We need this so our HTML frontend can call the API.

```python
from fastapi.responses import FileResponse
```
Allows FastAPI to return a file as an HTTP response. We use this to serve index.html.

```python
from app.api.routes.evaluate import router as evaluate_router
from app.api.routes.questions import router as questions_router
```
Import routers from route files. Renaming with `as` makes it clear what each router is.

```python
app = FastAPI(
    title="Interview Evaluator API",
    description="AI-powered interview answer evaluation system",
    version="1.0.0"
)
```
Create the FastAPI application. title, description, version appear in Swagger UI automatically.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```
Add CORS middleware:
`allow_origins=["*"]` — allow requests from any origin (wildcard). In production specify exact domains.
`allow_methods=["*"]` — allow all HTTP methods.
`allow_headers=["*"]` — allow all headers.

Without this, the browser blocks fetch requests from index.html to the API.

```python
app.include_router(evaluate_router)
app.include_router(questions_router)
```
Register both routers. Without these lines, POST /evaluate, GET /questions, GET /history do not exist.

```python
@app.get("/")
def root():
    return FileResponse("index.html")
```
The root endpoint returns index.html. When you open http://localhost:8000, FastAPI sends the HTML file. This serves the frontend through FastAPI — solving the file:// CORS problem.

---

## 12. `app/core/rag.py` — Every Line Explained

```python
from groq import Groq
```
Import the Groq API client class.

```python
import os
from dotenv import load_dotenv
```
For reading the GROQ_API_KEY from .env.

```python
load_dotenv()
```
Load .env into environment variables.

```python
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
```
Create the Groq client at module level. Created once when file is imported, reused across all requests. `os.getenv("GROQ_API_KEY")` fetches the API key from environment variables.

```python
def generate_feedback(question, user_answer, reference_answer, missing_concepts, score):
```
Five parameters: the question text, user's submitted answer, the correct reference answer from database, list of missing concepts, and the similarity score.

```python
    response = client.chat.completions.create(
```
Call the Groq API's chat completions endpoint. Send messages, receive a response.

```python
        model="llama-3.1-8b-instant",
```
Use LLaMA 3.1 with 8 billion parameters in Groq's instant (fast) mode.

```python
        messages=[
```
A list forming the conversation. LLMs work like a chat — you provide context and they continue it.

```python
            {
                "role": "system",
                "content": "You are an expert technical interviewer and educator. You are speaking directly to the candidate who just answered the question. Address them directly using 'you' and 'your'. Never refer to them as 'the user' or 'the candidate'."
            },
```
The system message sets the LLM's persona. `"role": "system"` is an instruction about how to behave.

This makes feedback say "Your answer captures..." instead of "The user's answer captures..." — direct address feels like a real mentor talking to you.

```python
            {
                "role": "user",
                "content": f"""
Question: {question}

Reference Answer: {reference_answer}

User's Answer: {user_answer}

Similarity Score: {score}/100

Missing Concepts: {', '.join(missing_concepts)}

Please provide:
1. SUGGESTIONS: 2-3 specific, constructive suggestions directly addressing the candidate using 'you' and 'your'
2. IMPROVED ANSWER: A professional, complete version of the answer

Format your response exactly like this:
SUGGESTIONS:
[your suggestions here]

IMPROVED ANSWER:
[improved answer here]
"""
            }
```
The user message is the AUGMENTED prompt. Breaking it down:

`f"""..."""` is a multi-line f-string. Variables in {curly braces} are replaced with actual values.

`{question}` becomes the actual question text.
`{reference_answer}` becomes the correct answer from your database — this is the RETRIEVAL result.
`{user_answer}` becomes what the user submitted.
`{score}` becomes the similarity number.
`{', '.join(missing_concepts)}` converts `["noise", "generalization"]` to `"noise, generalization"`.

The format instructions (SUGGESTIONS: and IMPROVED ANSWER: labels) are critical. They make the LLM response parseable by code. Without them the response is one paragraph that is hard to split.

```python
    result = response.choices[0].message.content
```
Extract the response text:
`response.choices` — list of responses (usually one).
`[0]` — first response.
`.message.content` — the actual text string.

```python
    return result
```
Return the full feedback string to the evaluate route.

---

## 13. `app/api/routes/evaluate.py` — Every Line Explained

```python
from fastapi import APIRouter, Depends
```
`APIRouter` — groups related endpoints. We define routes on a router and register the router with the main app.
`Depends` — FastAPI's dependency injection. Automatically calls get_db before the route runs.

```python
from sqlalchemy.orm import Session
```
Type hint for the db parameter.

```python
from app.db.session import get_db
from app.db.models import Question, ReferenceAnswer, Evaluation
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse
from app.core.embeddings import get_embedding
from app.core.similarity import compute_similarity
from app.core.rag import generate_feedback
```
All necessary imports. Every component of the pipeline is imported here.

```python
router = APIRouter()
```
Create the router instance.

```python
@router.post("/evaluate", response_model=EvaluationResponse)
```
Decorator: handle POST requests to /evaluate. `response_model` validates and documents the response.

```python
def evaluate(request: EvaluationRequest, db: Session = Depends(get_db)):
```
`request: EvaluationRequest` — FastAPI validates the JSON body against EvaluationRequest and passes it as a typed object.
`db: Session = Depends(get_db)` — FastAPI calls get_db automatically and passes the session as db.

```python
    user_embedding = get_embedding(request.user_answer)
```
Convert the user's answer text to a 384-dimensional vector.

```python
    reference = db.query(ReferenceAnswer)\
        .order_by(ReferenceAnswer.embedding.cosine_distance(user_embedding))\
        .first()
```
pgvector similarity search:

`db.query(ReferenceAnswer)` — SELECT from reference_answers.
`.order_by(ReferenceAnswer.embedding.cosine_distance(user_embedding))` — sort by cosine distance between each stored embedding and the user's embedding. Smallest distance (most similar) comes first. Uses pgvector's <=> operator.
`.first()` — return the closest match.

`reference` is a complete ReferenceAnswer object with all attributes.

```python
    similarity_score = compute_similarity(reference.embedding, user_embedding)
```
Raw cosine similarity score 0-100 between reference and user embeddings.

```python
    covered = [c for c in reference.key_concepts if c.lower() in request.user_answer.lower()]
    missing = [c for c in reference.key_concepts if c.lower() not in request.user_answer.lower()]
```
List comprehensions for concept detection.

`[c for c in reference.key_concepts if condition]` — create a list of concepts where condition is True.
`c.lower()` — lowercase the concept.
`request.user_answer.lower()` — lowercase the entire user answer.
`c.lower() in request.user_answer.lower()` — check if concept string appears anywhere in the answer. Case insensitive.

`covered` — concepts that appear.
`missing` — concepts that do not appear.

```python
    concept_score = (len(covered) / len(reference.key_concepts)) * 100 if reference.key_concepts else 0
```
Concept coverage as percentage:
`len(covered)` — how many concepts covered.
`len(reference.key_concepts)` — total concepts.
Division gives the ratio, multiplied by 100 gives percentage.
`if reference.key_concepts else 0` — avoid division by zero if concept list is empty.

```python
    score = round((similarity_score * 0.5) + (concept_score * 0.5), 2)
```
Weighted final score. 50% semantic similarity + 50% concept coverage. `round(..., 2)` for 2 decimal places.

```python
    question = db.query(Question).filter(Question.id == reference.question_id).first()
```
Fetch question text for the RAG prompt.
`.filter(Question.id == reference.question_id)` — WHERE id matches the question_id from the reference answer.

```python
    feedback = generate_feedback(
        question=question.text,
        user_answer=request.user_answer,
        reference_answer=reference.answer,
        missing_concepts=missing,
        score=similarity_score
    )
```
Call the RAG pipeline. We pass similarity_score (raw semantic score) rather than weighted score — the LLM feedback is more meaningful with the pure semantic similarity.

```python
    suggestions = ""
    improved_answer = ""
```
Initialize empty strings to be filled by parsing.

```python
    if "IMPROVED ANSWER:" in feedback:
        parts = feedback.split("IMPROVED ANSWER:")
        suggestions = parts[0].replace("SUGGESTIONS:", "").strip()
        improved_answer = parts[1].strip()
    else:
        suggestions = feedback
        improved_answer = ""
```
Parse LLM response:

`"IMPROVED ANSWER:" in feedback` — check if the LLM followed format instructions.
`feedback.split("IMPROVED ANSWER:")` — split at the separator into two parts.
`parts[0]` — everything before the separator (suggestions section).
`parts[1]` — everything after (improved answer).
`.replace("SUGGESTIONS:", "")` — remove the label.
`.strip()` — remove leading/trailing whitespace.

`else` handles cases where the LLM ignored format — puts everything in suggestions.

```python
    evaluation = Evaluation(
        question_id=reference.question_id,
        user_answer=request.user_answer,
        score=score,
        covered_concepts=covered,
        missing_concepts=missing,
        suggestions=suggestions,
        improved_answer=improved_answer
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
```
Create, save, and refresh the evaluation. Same pattern as seeding. db.refresh() gets the auto-generated id and created_at.

```python
    return EvaluationResponse(
        question_id=reference.question_id,
        score=score,
        covered_concepts=covered,
        missing_concepts=missing,
        suggestions=suggestions,
        improved_answer=improved_answer
    )
```
Return a typed response. FastAPI validates it against EvaluationResponse and converts to JSON.

---

## 14. `app/api/routes/questions.py` — Every Line Explained

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Question, Evaluation
from app.schemas.evaluation import QuestionResponse, HistoryResponse
```
Standard imports. QuestionResponse and HistoryResponse schemas for typed responses.

```python
router = APIRouter()
```

```python
@router.get("/questions", response_model=list[QuestionResponse])
```
GET endpoint. `list[QuestionResponse]` — response is a list of questions. FastAPI validates each item.

```python
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions
```
`db.query(Question).all()` — SELECT * FROM questions, return all rows as a list.
FastAPI maps each Question object to QuestionResponse automatically (id → id, text → text, domain → domain).

```python
@router.get("/history/{question_id}", response_model=list[HistoryResponse])
```
`{question_id}` in the path is a URL parameter. FastAPI extracts it automatically.

```python
def get_history(question_id: int, db: Session = Depends(get_db)):
    history = db.query(Evaluation).filter(Evaluation.question_id == question_id).all()
    return history
```
`question_id: int` — FastAPI converts the URL string to an integer.
`.filter(Evaluation.question_id == question_id)` — WHERE question_id = {the value from the URL}.
`.all()` — return all matching evaluations.

---

## 15. `index.html` — Every Section Explained

### HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
    <title>Interview Evaluator</title>
```
Standard HTML5 boilerplate. Title sets the browser tab name.

### CSS Styles

```css
body { font-family: Arial; max-width: 700px; margin: 40px auto; padding: 20px; }
```
Centers content in 700px column. `margin: 40px auto` — 40px top margin, auto left/right centers the block.

```css
.box { background: #f9f9f9; border: 1px solid #ddd; padding: 16px; margin-bottom: 12px; border-radius: 4px; }
```
Reusable class for result sections. Light gray background, subtle border, rounded corners.

```css
.tag { display: inline-block; padding: 3px 8px; margin: 2px; border-radius: 3px; font-size: 13px; }
.green { background: #e0ffe0; color: green; }
.red { background: #ffe0e0; color: red; }
```
Concept tag styles. `display: inline-block` lets tags sit next to each other. Green for covered, red for missing.

### The Form

```html
<select id="question">
    <option>Loading...</option>
</select>
```
Dropdown initially showing "Loading..." replaced by JavaScript when API loads questions.

```html
<textarea id="answer" placeholder="Type your answer here..."></textarea>
```
Multi-line text input for the answer.

```html
<button onclick="submitAnswer()">Evaluate</button>
```
Named `submitAnswer` (not `evaluate`) to avoid conflict with the built-in `document.evaluate()` browser method.

### JavaScript — Loading Questions

```javascript
fetch('http://localhost:8000/questions')
    .then(r => r.json())
    .then(data => {
        const select = document.getElementById('question');
        select.innerHTML = '<option value="">Choose a question...</option>';
        data.forEach(q => {
            select.innerHTML += `<option value="${q.text}">[${q.domain}] ${q.text}</option>`;
        });
    });
```
`fetch(url)` makes an HTTP GET request. Returns a Promise.
`.then(r => r.json())` parses the response as JSON when it arrives.
`.then(data => {...})` runs when parsing is complete. `data` is the array of question objects.
`document.getElementById('question')` finds the select element.
`data.forEach(q => {...})` loops through each question.
Template literal creates HTML option elements. The `value` is the question text — sent to the API when selected.

### JavaScript — Evaluating

```javascript
async function submitAnswer() {
    const question = document.getElementById('question').value;
    const answer = document.getElementById('answer').value;
```
`async` — required because we use `await` inside.
`.value` gets the current value from each form element.

```javascript
    if (!question || !answer) {
        document.getElementById('status').textContent = 'Please select a question and write an answer.';
        return;
    }
```
Validation. `!question` is true if empty. Show error and stop.

```javascript
    const res = await fetch('http://localhost:8000/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, user_answer: answer })
    });
```
`await` waits for the request to complete.
`method: 'POST'` — POST request.
`'Content-Type': 'application/json'` — tell server we are sending JSON.
`JSON.stringify({...})` — convert JavaScript object to JSON string. `{ question, user_answer: answer }` maps the `answer` variable to `user_answer` key matching EvaluationRequest schema.

```javascript
    const data = await res.json();
```
Parse response body as JSON.

```javascript
    document.getElementById('covered').innerHTML = data.covered_concepts.map(c => `<span class="tag green">${c}</span>`).join('');
```
`.map(c => ...)` transforms each concept string into an HTML span element.
`.join('')` joins all spans into one string.
`.innerHTML = ...` renders the HTML (not plain text).

```javascript
    document.getElementById('suggestions').textContent = data.suggestions;
    document.getElementById('improved').textContent = data.improved_answer;
```
`textContent` (not innerHTML) for plain text. Prevents any HTML in LLM output from being rendered as HTML.

---

## 16. Database Design — Every Decision Explained

### Why Three Tables Not One

One big table would repeat question and reference data for every evaluation. Three tables with foreign keys:
- Store each question once in questions table
- Store each reference answer once in reference_answers table
- Store each evaluation in evaluations table, linked by foreign keys

This is proper database normalization — no repeated data.

### Why Foreign Keys

Foreign keys enforce data integrity at the database level:
- Cannot insert a reference_answer with a question_id that does not exist
- Cannot delete a question that has linked reference answers or evaluations
- PostgreSQL prevents orphaned data automatically

### Why JSON for Lists

key_concepts, covered_concepts, missing_concepts are all lists of strings. PostgreSQL's JSON type stores them natively with proper list-to-database-to-list conversion. The alternative (a separate concepts table) adds complexity for no benefit at this scale.

### Why Vector(384)

MiniLM always outputs 384-dimensional vectors — this is fixed by the model architecture. The database column dimension must match exactly.

### Why server_default Instead of Python datetime.now()

`server_default=func.now()` tells PostgreSQL to set the timestamp. The database is always the authoritative time source — consistent regardless of application server timezone or configuration. Python's `datetime.utcnow()` was deprecated in newer versions and relies on application-side time.

---

## 17. The ML Pipeline — How It All Connects

End-to-end example:

User submits: "Overfitting is when training accuracy is high but test is low"

Step 1 — Embedding:
```
get_embedding("Overfitting is when training accuracy is high but test is low")
MiniLM processes → [0.25, -0.79, 0.41, ...] (384 numbers)
```

Step 2 — pgvector Search:
```
SELECT * FROM reference_answers 
ORDER BY embedding <=> [0.25, -0.79, 0.41, ...]
LIMIT 1
→ Returns: reference answer for "What is overfitting?" with its embedding, answer text, key concepts
```

Step 3 — Cosine Similarity:
```
compute_similarity([0.23, -0.81, ...], [0.25, -0.79, ...])
cosine_similarity returns 0.8712
float(0.8712) * 100 = 87.12
```

Step 4 — Concept Detection:
```
key_concepts = ["noise", "training data", "unseen data", "generalization", "regularization", ...]
user_answer = "overfitting is when training accuracy is high but test is low"

"noise" in answer? No → missing
"training data" in answer? No (has "training" but not "training data") → missing
"unseen data" in answer? No → missing
...

covered = []
missing = ["noise", "training data", "unseen data", ...]
```

Step 5 — Weighted Score:
```
similarity_score = 87.12
concept_score = (0/8) * 100 = 0
final_score = (87.12 * 0.5) + (0 * 0.5) = 43.56
```

This is much more accurate than pure similarity. A short semantically-close answer gets a low score if it covers no concepts.

---

## 18. The RAG Pipeline — How It All Connects

### Why RAG

Without RAG, sending "evaluate this answer" to the LLM produces generic feedback based on the LLM's training knowledge. The LLM guesses what a good answer looks like. This is hallucination.

With RAG:
1. RETRIEVE the correct reference answer from your database
2. AUGMENT the prompt with that real reference data
3. GENERATE feedback grounded in your specific data

The LLM sees the exact correct answer and exact missing concepts. Feedback is specific, not generic.

### The Prompt Construction

```python
f"""
Question: {question}           ← the actual question text
Reference Answer: {reference}  ← RETRIEVED from database
User's Answer: {user_answer}   ← what they submitted
Similarity Score: {score}/100  ← computed by ML pipeline
Missing Concepts: {', '.join(missing_concepts)}  ← detected by concept check

SUGGESTIONS: ...
IMPROVED ANSWER: ...
"""
```

Every piece of context comes from either the database or the ML pipeline. The LLM has no need to guess anything.

### Why Format Instructions Are Critical

Without: "Your answer shows basic understanding but lacks depth. You should mention noise and generalization. Here is a better version: Overfitting occurs when..."

This is one paragraph. Hard to split into suggestions vs improved answer reliably.

With format instructions: "SUGGESTIONS:" and "IMPROVED ANSWER:" as clear labels means splitting on "IMPROVED ANSWER:" always works:
```python
parts = feedback.split("IMPROVED ANSWER:")
suggestions = parts[0].replace("SUGGESTIONS:", "").strip()
improved_answer = parts[1].strip()
```

---

## 19. Every Error We Faced and How We Fixed It

### Error 1: pgvector Extension Not Available

Full error:
```
ERROR: extension "vector" is not available
HINT: The extension must first be installed on the system
```

Root cause: pgvector is not included in standard PostgreSQL. Our local PostgreSQL 18 on Windows did not have it. pgvector requires separate installation — difficult on Windows with newer PostgreSQL versions.

Important distinction: Python's `pgvector` package (pip install pgvector) and PostgreSQL's pgvector extension are completely separate things. The Python package teaches SQLAlchemy to understand Vector column types. The PostgreSQL extension adds the Vector type to the database itself. Both are required.

Diagnosis: Error message was clear. Tried Stack Builder (PostgreSQL's GUI tool) but pgvector was not listed. pip install pgvector only installed the Python side, not the PostgreSQL side.

Fix: Used Docker with the official pgvector pre-built image:
```bash
docker run --name pgvector-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=interview_evaluator -p 5432:5432 -d pgvector/pgvector:pg16
```

Verification:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
-- Result: CREATE EXTENSION (success)
```

Lesson: When a system dependency causes compatibility issues, Docker with a pre-configured image is often the cleanest solution. It eliminates the local installation problem entirely.

---

### Error 2: Password Authentication Failed (Occurred Twice)

Full error:
```
FATAL: password authentication failed for user "postgres"
```

Root cause: Local PostgreSQL (installed on Windows) starts automatically on boot and runs on port 5432. When code connects to localhost:5432, it reaches local PostgreSQL (wrong password) instead of Docker (correct password). Two services cannot share a port.

First occurrence: During alembic revision command.
Second occurrence: After computer restart, local PostgreSQL auto-started again.

Diagnosis: Password in .env was correct. Docker was running. Process of elimination — port conflict. Diagnostic command: `netstat -ano | findstr :5432` shows which processes use port 5432.

Fix:
1. Opened services.msc (Win+R → services.msc)
2. Found PostgreSQL service
3. Right-clicked → Stop
4. Right-clicked → Properties → Startup type → Manual (prevents auto-start on boot)

Lesson: "Password authentication failed" with correct credentials means you are connecting to the wrong service. Always check for port conflicts first. Two services cannot share one port.

---

### Error 3: pgvector Not Defined in Migration File

Full error:
```
NameError: name 'pgvector' is not defined
LINE 1: ...embedding', pgvector.sqlalchemy.vector.VECTOR(dim=384)...
```

Root cause: Alembic's autogenerate wrote the Vector column as `pgvector.sqlalchemy.vector.VECTOR(dim=384)` but did not add `import pgvector` at the top of the migration file. Python does not know what `pgvector` means without the import.

Diagnosis: NameError always means something was used without being imported. Checked the migration file imports — only standard sqlalchemy imports, no pgvector.

Fix: Manually edited the migration file:
1. Added import at top:
```python
from pgvector.sqlalchemy import Vector
```
2. Changed column definition:
```python
# From:
pgvector.sqlalchemy.vector.VECTOR(dim=384)
# To:
Vector(384)
```

Lesson: Alembic autogenerate works for standard types but sometimes fails for third-party types. Always review autogenerated migration files before running. `NameError: name 'X' is not defined` ALWAYS means X was never imported.

---

### Error 4: numpy float64 Type Error

Full error:
```
psycopg2.errors.InvalidSchemaName: schema "np" does not exist
LINE 1: ...score', np.float64(87.12)...
```

Root cause: scikit-learn returns numpy float64 values. When SQLAlchemy tried to insert `np.float64(87.12)` into PostgreSQL, the driver did not recognize it as a number. It tried to interpret `np` as a PostgreSQL schema name.

Diagnosis: The SQL in the error message showed `np.float64(87.12)` — numpy's string representation was being sent as a literal value to PostgreSQL. This revealed the type was not being converted.

Fix: Wrap score in `float()` in similarity.py:
```python
return round(float(score) * 100, 2)
```
`float()` converts numpy float64 to a plain Python float.

Lesson: numpy types are NOT Python types despite looking similar. Always convert when storing in databases:
- `float(numpy_float)` for floats
- `int(numpy_int)` for integers  
- `array.tolist()` for arrays

This is one of the most common bugs when mixing numpy with databases.

---

### Error 5: Swagger UI Showing Old Schema

What happened: After adding suggestions and improved_answer to EvaluationResponse, the API response still did not include them. Even downloaded JSON files were missing the fields. Hardcoded test values also did not appear.

Root cause: Python compiles .py files to bytecode stored in __pycache__ folders. FastAPI was loading the cached compiled version of evaluation.py that did not have the new fields.

Diagnosis: Checked http://localhost:8000/openapi.json — the schema did not contain suggestions or improved_answer. This confirmed FastAPI was reading old cached schema. Since the code was correct, the issue was cached bytecode.

Fix:
```powershell
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
```
Then restart uvicorn.

Lesson: When code changes do not take effect, Python cache is often the culprit. Always check /openapi.json to verify what FastAPI has actually loaded. Clearing __pycache__ forces Python to recompile everything fresh.

---

### Error 6: CORS Blocking Frontend

What happened: Opening index.html as a file:// URL showed "Failed to load — is the API running?" The API was running fine.

Root cause: Browsers enforce the Same-Origin Policy. A file:// URL is a unique security origin. Requests from file:// to http://localhost:8000 are cross-origin and blocked. CORS errors appeared in the browser console (F12).

Fix part 1 — Add CORSMiddleware to FastAPI:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Fix part 2 — Serve index.html through FastAPI:
```python
@app.get("/")
def root():
    return FileResponse("index.html")
```
Now frontend at http://localhost:8000 and API at http://localhost:8000/evaluate are the same origin — no CORS issue.

Lesson: Never open HTML files directly with file:// when they need to make API calls. Serve through a web server. Use the browser console (F12 → Console tab) to diagnose frontend issues.

---

### Error 7: "evaluate" JavaScript Reserved Name

Full error:
```
Uncaught TypeError: Failed to execute 'evaluate' on 'Document': 
2 arguments required, but only 0 present.
```

Root cause: The browser's document object has a built-in method called evaluate() used for XPath queries. The button `onclick="evaluate()"` resolved to `document.evaluate()` (the built-in) instead of our custom function.

Diagnosis: Error said document.evaluate() requires 2 arguments. Our function took 0 — wrong number revealed it was calling the built-in.

Fix: Renamed function to `submitAnswer()`:
```html
<button onclick="submitAnswer()">Evaluate</button>
```

Lesson: Avoid naming JavaScript functions the same as built-in browser methods. Common conflicts: evaluate, open, close, print, focus, blur, name, status.

---

### Error 8: Score Inflated for Incomplete Answers

What happened: "Supervised learning is a type of machine learning where model learns from data" scored 86/100. Zero key concepts covered.

Root cause: Pure cosine similarity measures semantic closeness not completeness. The sentence opening is nearly identical to the reference answer opening. The embedding captures this high similarity even though all key content is missing.

Fix: Weighted scoring:
```python
similarity_score = compute_similarity(reference.embedding, user_embedding)
concept_score = (len(covered) / len(reference.key_concepts)) * 100
score = round((similarity_score * 0.5) + (concept_score * 0.5), 2)
```
Same answer now scores 18/100 — accurately reflecting its incomplete nature.

Lesson: Single-metric evaluation is almost always insufficient. When a system produces counterintuitive results, investigate the root cause and improve the metric design.

---

## 20. Interview Questions — What If Scenarios

**Q: What if the user asks a question not in the database?**

pgvector still returns the closest reference answer — it does not require exact matches. But evaluation quality degrades if the submitted question is completely different from any stored question.

Proper solution (future improvement): Check similarity between submitted question and stored questions. If below a threshold (say 0.5), generate a reference dynamically via LLM, cache it in the database, and proceed with evaluation.

---

**Q: What if the LLM does not follow the SUGGESTIONS/IMPROVED ANSWER format?**

The else branch handles this:
```python
else:
    suggestions = feedback
    improved_answer = ""
```
All feedback goes into suggestions. Evaluation still completes — score and concepts are unaffected. User sees suggestions but no improved answer.

---

**Q: What if two users evaluate simultaneously?**

FastAPI handles concurrent requests correctly. Each request gets its own database session from get_db. SQLAlchemy manages connection pooling. PostgreSQL uses row-level locking for concurrent writes. No data corruption or race conditions.

---

**Q: What if the Groq API is down?**

Currently returns a 500 error. Production fix:
```python
try:
    feedback = generate_feedback(...)
except Exception:
    suggestions = "Feedback temporarily unavailable. Please try again."
    improved_answer = ""
```
Score and concepts still returned even when LLM fails.

---

**Q: What if a user submits a very long answer?**

MiniLM has a maximum of 256 word pieces. Longer answers are silently truncated before embedding. Concept detection still works on full text (string matching). For very long answers the semantic score may be less accurate.

Fix: Chunk long answers, embed each chunk, average the embeddings. Or use a model with a longer context window.

---

**Q: What if the database grows to 100,000 questions?**

Add an HNSW index to make similarity search logarithmic instead of linear:
```sql
CREATE INDEX ON reference_answers USING hnsw (embedding vector_cosine_ops);
```
pgvector handles millions of vectors with proper indexing. Without an index, every search scans every row.

---

**Q: What if concept detection misses a concept because the user used synonyms?**

Known limitation. Current detection is keyword-based. "The model generalizes well" does not match "generalization" as a concept.

Proper fix: Embedding-based concept detection. Generate embeddings for each key concept. Check cosine similarity between concept embedding and user answer segments. If above a threshold, mark as covered. This catches paraphrases and synonyms.

---

**Q: What if you want to add user accounts?**

Add a users table and link evaluations to users:
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
```
Add JWT authentication endpoints. Add user_id foreign key to Evaluation. Filter history by both question_id and user_id.

---

## 21. Interview Questions — Why Not This Instead

**Q: Why not LangChain for RAG?**

LangChain abstracts retrieval and prompt construction into high-level calls. You call chain.run() without knowing what happens underneath. We built every step manually:
- The pgvector similarity search (retrieval)
- The f-string prompt construction (augmentation)
- The Groq API call (generation)
- The response parsing (extraction)

Every line can be explained. In an interview "I built the RAG pipeline manually to understand the internals" is significantly stronger than "I used LangChain." Understanding the primitives is more valuable than knowing an abstraction.

---

**Q: Why not OpenAI embeddings?**

Three reasons:
1. Cost — OpenAI charges per API call. Development generates hundreds of embedding calls.
2. Latency — requires a network call. MiniLM runs locally, instant.
3. Privacy — user answers leave your machine with OpenAI. MiniLM runs entirely locally.

MiniLM's 384-dimensional embeddings are perfectly sufficient for semantic similarity on technical answers.

---

**Q: Why not Pinecone instead of pgvector?**

For our scale (hundreds of questions), pgvector in PostgreSQL is architecturally simpler and equally performant.

Pinecone adds: a separate paid service, separate API keys, separate connection management, external network latency, monthly cost.

pgvector gives: vector storage alongside relational data, same database connection, same transactions, free, faster (no external call).

The engineering principle: do not add infrastructure you do not need. Pinecone makes sense at millions of vectors with very high query concurrency.

---

**Q: Why FastAPI over Flask?**

Flask requires manual request parsing, separate validation library, separate documentation library, no async by default.

FastAPI provides automatic Pydantic validation, auto-generated Swagger UI from schemas, async by default, faster performance. For ML APIs FastAPI is the modern industry standard.

---

**Q: Why SQLAlchemy over raw SQL?**

Raw SQL in Python strings: injection risk, verbose, hard to refactor, no type safety.

SQLAlchemy: parameterized queries prevent injection, Pythonic and readable, type-safe, supports Alembic migrations.

---

**Q: Why Docker instead of installing PostgreSQL locally?**

Our local PostgreSQL 18 did not support pgvector on Windows. Docker provided a pre-built image that works immediately.

General answer: Docker provides reproducible environments. "It works on my machine" is a classic problem. With Docker, anyone who clones the project runs one command and gets the exact same setup.

---

**Q: Why not Django?**

Django is a full-stack framework for web applications — HTML templates, admin panels, ORM tightly coupled to the framework. We are building a pure REST API. Django adds massive unnecessary complexity. FastAPI is purpose-built for APIs.

---

**Q: Why not MongoDB?**

Our data is relational:
- Questions have reference answers (one-to-many)
- Questions have evaluations (one-to-many)
- Foreign keys enforce these at the database level

MongoDB would require manual relationship management, no pgvector support, loss of typed columns. There is no advantage to NoSQL here.

---

**Q: Why not add authentication?**

Authentication was deprioritized to keep focus on the ML and RAG components — the core technical value. JWT auth is important but boilerplate. Adding it requires a users table, register/login endpoints, token generation/validation, and protected routes. This is clearly noted as a future improvement.

---

## 22. How to Start the Project Every Time

Every time you work on this project run these commands in this exact order:

### Step 1 — Navigate to Project Folder
```bash
cd C:\Users\dell\Desktop\ML\interview-evaluator
```

### Step 2 — Activate Virtual Environment
```bash
venv\Scripts\activate
```
Confirm (venv) appears at the start of your terminal. Without activation, uvicorn cannot find installed packages.

### Step 3 — Start Docker Container
```bash
docker start pgvector-db
```
Container stops when computer shuts down. This starts it again. Open Docker Desktop first if it is not running.

### Step 4 — Start the API
```bash
uvicorn app.main:app --reload
```
Wait for: `INFO: Application startup complete.`

### Step 5 — Open the App
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

### Troubleshooting

**"Password authentication failed":**
Local PostgreSQL is running on port 5432. Open services.msc → find PostgreSQL → Stop it. Then retry.

**Schema changes not reflected:**
```powershell
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
```
Restart uvicorn.

**Questions not loading in frontend:**
Check uvicorn is running. Check Docker is running (`docker ps`). Open browser console (F12) for error messages.

**After changing database models:**
```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

**To clear all test data and re-seed:**
```bash
docker exec -it pgvector-db psql -U postgres -d interview_evaluator
```
```sql
TRUNCATE TABLE evaluations, reference_answers, questions RESTART IDENTITY CASCADE;
\q
```
```bash
python seed.py
```

**To push code changes to GitHub:**
```bash
git add .
git commit -m "describe your changes"
git push
```

---

*Complete documentation for every line of code, every decision, and every error.*
*Built by Moiz Nisar — AI-Powered Interview Answer Evaluator*
*FastAPI + PostgreSQL + pgvector + sentence-transformers + Groq LLaMA 3*
