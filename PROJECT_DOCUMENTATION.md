# Complete Project Documentation
# AI-Powered Interview Preparation System
# Built by Moiz Nisar

---

## Table of Contents

**Part 1 — Initial Build**
1. Project Overview
2. Tools and Technologies
3. Project Setup
4. app/db/session.py
5. app/db/models.py
6. alembic/env.py
7. app/core/embeddings.py
8. app/core/similarity.py
9. seed.py
10. app/schemas/evaluation.py
11. app/main.py
12. app/core/rag.py
13. app/api/routes/evaluate.py
14. app/api/routes/questions.py
15. index.html (original)
16. Database Design
17. The ML Pipeline
18. The RAG Pipeline

**Part 2 — Upgrades and Improvements**
19. Why We Made Changes
20. Fix 1 — Improved Answer Length and Tone
21. Fix 2 — Conversational Key Concepts
22. Fix 3 — Python-Generated Suggestions
23. Fix 4 — Weighted Scoring
24. New Feature — Difficulty Column
25. New Feature — 40 Questions Across 7 Domains
26. New Feature — Random Question Order
27. New Feature — MCQ Mode (Full Explanation)
28. New Feature — Updated Frontend

**Part 3 — Reference**
29. Every Error We Faced and How We Fixed It
30. Interview Questions — What If Scenarios
31. Interview Questions — Why Not This Instead
32. How to Start the Project Every Time

---

# PART 1 — INITIAL BUILD

---

## 1. Project Overview

### What We Built

An AI-Powered Interview Answer Evaluation System. When a user submits a technical
interview answer the system converts it to a vector embedding, searches a PostgreSQL
database with pgvector for the closest reference answer, computes a weighted similarity
score, detects covered and missing key concepts, generates improvement suggestions, sends
everything to LLaMA 3 via Groq to generate a concise improved answer, saves the
evaluation, and returns everything as a clean JSON response.

### What Problem It Solves

When someone prepares for technical interviews they write answers but have no way to know
how correct their answer is, what key concepts they missed, how to specifically improve,
or what a professional version sounds like. This system solves all four automatically.

### Why This Project Is Strong

Combines real ML (embeddings, cosine similarity, vector search) with a production-grade
API. Implements RAG architecture manually without LangChain. Uses pgvector for vector
storage. Shows proper database design with foreign keys and migrations. Every technical
decision can be explained and defended in an interview.

---

## 2. Tools and Technologies

### FastAPI
A modern Python web framework for building REST APIs. Auto-generates Swagger UI,
has built-in Pydantic validation, supports async. The modern industry standard for
ML APIs. Not Flask (no auto-docs, no validation) and not Django (full-stack framework,
overkill for a pure API).

### PostgreSQL + pgvector
PostgreSQL is the relational database. pgvector is an extension adding a VECTOR column
type and cosine distance search. Keeps vector data and relational data in one database.
Not Pinecone or Chroma — separate paid services with no benefit at our scale (hundreds
of questions). pgvector is free, integrated, and sufficient.

### SQLAlchemy + Alembic
SQLAlchemy translates between Python objects and PostgreSQL tables (ORM). Alembic tracks
schema changes as versioned migration files — like Git for your database. Every change is
reversible. Anyone who clones the project runs `alembic upgrade head` and gets the same schema.

### sentence-transformers (MiniLM all-MiniLM-L6-v2)
Generates 384-dimensional vector embeddings from text. Free, runs locally, no API cost,
no data leaves your machine. Not OpenAI embeddings (costs money per call) and not
Word2Vec (word-level, we need sentence-level).

### scikit-learn
Used for exactly one function — cosine_similarity. Reliable tested implementation.

### Groq API with LLaMA 3 (llama-3.1-8b-instant)
Free tier, sub-second inference, strong model. Not OpenAI (costs money). Not local LLM
with Ollama (requires 8-16GB RAM, slow without GPU).

### Docker
Runs PostgreSQL + pgvector in an isolated container. pgvector could not be installed
on local PostgreSQL 18 on Windows. The pre-built pgvector/pgvector:pg16 image has
everything ready in one command.

### Pydantic
Automatic request/response validation. Wrong input is rejected before reaching your
code. Auto-generates Swagger UI documentation. Write zero validation code manually.

---

## 3. Project Setup

### Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

Isolated Python installation for this project. Prevents package version conflicts
between different projects. Every pip install goes into the project's private space.

### Installing Dependencies

```bash
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary pgvector \
            sentence-transformers scikit-learn python-dotenv groq
```

- fastapi — API framework
- uvicorn — server that runs FastAPI (the engine)
- sqlalchemy — ORM translating Python to PostgreSQL
- alembic — database migration tool
- psycopg2-binary — actual PostgreSQL driver (the USB cable, never touched directly)
- pgvector — teaches SQLAlchemy about Vector column types
- sentence-transformers — MiniLM embedding model
- scikit-learn — cosine_similarity
- python-dotenv — reads .env file
- groq — Groq API client

```bash
pip freeze > requirements.txt
```

Saves exact versions. Anyone clones and runs `pip install -r requirements.txt`.

### Docker Container

```bash
docker run --name pgvector-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=interview_evaluator \
  -p 5432:5432 \
  -d pgvector/pgvector:pg16
```

- --name pgvector-db — container name for later reference
- -e POSTGRES_PASSWORD=postgres — database password
- -e POSTGRES_DB=interview_evaluator — auto-creates this database
- -p 5432:5432 — maps Windows port 5432 to container port 5432
- -d — runs in background
- pgvector/pgvector:pg16 — pre-built image with PostgreSQL 16 + pgvector

### Alembic Init

```bash
alembic init alembic
```

Creates alembic/ folder, env.py, script.py.mako, alembic.ini. One-time setup.

### Running Migrations

```bash
alembic revision --autogenerate -m "description"
```
Compares SQLAlchemy models against actual database, generates migration file.

```bash
alembic upgrade head
```
Applies all pending migrations. Tables physically created in PostgreSQL.

### Running the API

```bash
uvicorn app.main:app --reload
```
- app.main — find app/ folder, then main.py inside it
- :app — use the variable named app inside main.py
- --reload — restart automatically when you save any Python file

---

## 4. app/db/session.py — Every Line Explained

```python
from dotenv import load_dotenv
```
Import load_dotenv from python-dotenv. Reads .env file and loads values into OS
environment variables.

```python
from sqlalchemy import create_engine
```
Import create_engine. Creates the actual database connection.

```python
from sqlalchemy.orm import sessionmaker, declarative_base
```
sessionmaker — factory that creates database sessions.
declarative_base — creates the Base class all models inherit from.

```python
import os
```
Python's built-in os module for reading environment variables.

```python
load_dotenv()
```
Reads .env file. Loads DATABASE_URL, GROQ_API_KEY, SECRET_KEY into OS environment.
Without this, os.getenv() finds nothing.

```python
DATABASE_URL = os.getenv("DATABASE_URL")
```
"DATABASE_URL" in quotes — a string key you are searching for in environment variables.
DATABASE_URL without quotes — the variable that stores the result.
Result: "postgresql://postgres:postgres@localhost:5432/interview_evaluator"
Breaking down the URL: postgresql (driver) :// postgres (user) : postgres (password)
@ localhost (host) : 5432 (port) / interview_evaluator (database)

```python
engine = create_engine(DATABASE_URL)
```
Creates the engine using the URL variable (not the text "DATABASE_URL"). The engine
is the actual connection — the phone line between Python and PostgreSQL.

```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```
Session factory. autocommit=False means you control when to save. autoflush=False
means you control when queries are sent. bind=engine means sessions use our engine.

```python
Base = declarative_base()
```
The Base class. Every model inherits from this. Inheriting from Base tells SQLAlchemy
this class represents a database table. Base.metadata contains all table definitions
— Alembic reads this to detect changes.

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
FastAPI dependency. yield (not return) pauses the function and passes db to the route.
Route runs. When done, function resumes and finally closes the session. Always closes
even if an error occurs. Without this, connections pile up and the database crashes.

---

## 5. app/db/models.py — Every Line Explained

```python
from app.db.session import Base
```
Import the same Base instance. All models must use the same Base to be registered
in Base.metadata together.

```python
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float, DateTime, func
```
Column — defines a column. Integer, String, Float, DateTime — data types.
ForeignKey — links to another table's column. JSON — stores Python lists as JSON.
func — SQL functions, used for func.now() automatic timestamps.

```python
from pgvector.sqlalchemy import Vector
```
Imports the Vector column type from pgvector. Without pgvector installed this fails.

### Question Model

```python
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    difficulty = Column(String, nullable=False, server_default="easy")
```
__tablename__ — actual PostgreSQL table name.
primary_key=True — unique identifier, auto-incremented by PostgreSQL.
nullable=False — column cannot be empty, PostgreSQL enforces this.
server_default="easy" — PostgreSQL sets this automatically if not provided.

### ReferenceAnswer Model

```python
class ReferenceAnswer(Base):
    __tablename__ = "reference_answers"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer = Column(String, nullable=False)
    key_concepts = Column(JSON, nullable=False)
    embedding = Column(Vector(384), nullable=False)
    options = Column(JSON, nullable=True)
```
ForeignKey("questions.id") — links each reference answer to a question. PostgreSQL
enforces this — you cannot insert a reference_answer with a non-existent question_id.
Vector(384) — pgvector column storing 384 floating point numbers. The 384 must match
MiniLM's output dimension exactly.
options — nullable=True because it was added later and existing rows have NULL.

### Evaluation Model

```python
class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_answer = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    covered_concepts = Column(JSON, nullable=False)
    missing_concepts = Column(JSON, nullable=False)
    suggestions = Column(String, nullable=False)
    improved_answer = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
```
Float — stores decimals like 87.12.
JSON — stores Python lists as JSON arrays in PostgreSQL.
server_default=func.now() — PostgreSQL sets the timestamp automatically. More reliable
than Python-side datetime because it uses the database server's time regardless of
application server timezone.

---

## 6. alembic/env.py — Every Change Explained

### Change 1 — Load Database URL from .env

```python
config = context.config  # already existed

from dotenv import load_dotenv
import os
load_dotenv()
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
```

Overrides the sqlalchemy.url in alembic.ini with the value from .env. Database URL
lives in one place. Password never hardcoded in tracked files.

### Change 2 — Point to Models

```python
# Before
target_metadata = None

# After
from app.db.models import Base
target_metadata = Base.metadata
```

Base.metadata contains the complete definition of all three tables. With None, Alembic
is blind and generates empty migrations. With Base.metadata, it compares your models
against the actual database and generates accurate migrations.

---

## 7. app/core/embeddings.py — Every Line Explained

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
```
Loaded at MODULE LEVEL — outside any function. Runs once when the file is first
imported. Downloads ~90MB on first run, loads from cache instantly after.
If inside the function, it reloads on every API request — catastrophically slow.

```python
def get_embedding(text):
    return model.encode(text).tolist()
```
model.encode(text) — runs text through MiniLM, returns numpy array of 384 numbers.
.tolist() — converts numpy array to plain Python list. pgvector expects a Python list.
Numpy arrays look similar but are a different type PostgreSQL does not understand.

---

## 8. app/core/similarity.py — Every Line Explained

```python
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(embedding1, embedding2):
    score = cosine_similarity([embedding1], [embedding2])[0][0]
    return round(float(score) * 100, 2)
```
[embedding1] and [embedding2] — wrapping in brackets creates 2D arrays as sklearn
expects for pairs of vectors.
cosine_similarity returns [[0.8712]] — a nested array.
[0][0] extracts the plain float.
float(score) — CRITICAL. Converts numpy float64 to plain Python float. Without this,
PostgreSQL raises "schema np does not exist" because it cannot understand numpy types.
* 100 — converts 0-1 range to 0-100 scale.
round(..., 2) — 2 decimal places.

---

## 9. seed.py — Every Line Explained

```python
from app.db.session import SessionLocal
from app.db.models import Question, ReferenceAnswer
from app.core.embeddings import get_embedding
```
Import session factory, models, and embedding function.

```python
db = SessionLocal()
if db.query(Question).first():
    print("Database already seeded")
    db.close()
    exit()
```
Opens a session. Checks if any questions exist. If yes, exits to prevent duplicates.
Always closes the session even when exiting early.

```python
for item in questions_data:
    question = Question(
        text=item["question"],
        domain=item["domain"],
        difficulty=item["difficulty"]
    )
    db.add(question)
    db.commit()
    db.refresh(question)
```
Creates Python object. db.add() queues it. db.commit() saves to PostgreSQL and
PostgreSQL assigns an id. db.refresh() fetches that id back into the Python object.
CRITICAL — without refresh, question.id is None and the foreign key fails.

```python
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
db.close()
```
Generates embedding, creates reference answer linking to the question via question.id,
saves, prints progress, closes session when done.

---

## 10. app/schemas/evaluation.py — Every Line Explained

```python
from pydantic import BaseModel
from datetime import datetime

class EvaluationRequest(BaseModel):
    question: str
    user_answer: str
```
Defines what POST /evaluate must receive. If user sends wrong types or missing fields,
FastAPI automatically returns 422 Validation Error. Zero manual validation code.

```python
class EvaluationResponse(BaseModel):
    question_id: int
    score: float
    covered_concepts: list
    missing_concepts: list
    suggestions: str
    improved_answer: str
```
Defines what POST /evaluate returns. FastAPI validates your return value against this.
Also auto-generates Swagger UI documentation.

```python
class MCQRequest(BaseModel):
    question_id: int
    selected_option: str

class MCQResponse(BaseModel):
    correct: bool
    selected_option: str
    correct_answer: str
    explanation: str
```
MCQ mode schemas. question_id instead of question text because MCQ needs exact options
for a specific question — text search could match the wrong question.

```python
class QuestionResponse(BaseModel):
    id: int
    text: str
    domain: str

class HistoryResponse(BaseModel):
    id: int
    user_answer: str
    score: float
    covered_concepts: list
    missing_concepts: list
    created_at: datetime
```
Shapes for GET /questions and GET /history responses.

---

## 11. app/main.py — Every Line Explained

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.api.routes.evaluate import router as evaluate_router
from app.api.routes.questions import router as questions_router
```
Import FastAPI, CORS middleware, FileResponse for serving HTML, and both routers.

```python
app = FastAPI(
    title="Interview Evaluator API",
    description="AI-powered interview answer evaluation system",
    version="1.0.0"
)
```
Creates the application. title, description, version appear in Swagger UI.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```
CORS — Cross-Origin Resource Sharing. Browsers block requests from one origin to
another by default. The frontend at http://localhost:8000 and the API at
http://localhost:8000/evaluate are the same origin so this mainly helps during
development and for any future external frontend.

```python
app.include_router(evaluate_router)
app.include_router(questions_router)
```
Registers all routes from both routers. Without these lines the endpoints do not exist.

```python
@app.get("/")
def root():
    return FileResponse("index.html")
```
Returns index.html when browser visits the root URL. This serves the frontend through
FastAPI — solving the file:// CORS problem. Opening HTML directly as file:// blocks
API calls. Serving through FastAPI makes them the same origin.

---

## 12. app/core/rag.py — Every Line Explained

```python
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
```
Creates Groq client at module level. Created once, reused across all requests.

```python
def generate_feedback(question, user_answer, reference_answer, missing_concepts, score):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful senior engineer giving feedback to a junior developer preparing for a technical job interview. You speak simply and directly — like a real person, not a textbook."
            },
            {
                "role": "user",
                "content": f"""
Question: {question}
Reference Answer: {reference_answer}
User's Answer: {user_answer}
Similarity Score: {score}/100
Missing Concepts: {', '.join(missing_concepts)}

IMPORTANT: Only address Missing Concepts listed above. Do NOT suggest adding
something already in the user's answer.

RULES:
- IMPROVED ANSWER only: exactly 3 sentences, simple words, interview speech style

EXAMPLE OF WHAT NOT TO DO:
IMPROVED ANSWER:
Overfitting occurs when a model learns to the extent that it negatively impacts
performance on unseen data distributions due to high variance.

EXAMPLE OF WHAT TO DO:
IMPROVED ANSWER:
Overfitting is when a model memorizes the training data too well including the noise
so it fails on new data. It performs well on training but poorly on test data.
You can prevent it using regularization, cross-validation, and early stopping.

Format exactly like this:
IMPROVED ANSWER:
[3 sentences]
"""
            }
        ]
    )
    result = response.choices[0].message.content
    return result
```

The system message sets the LLM's persona — helpful senior engineer, simple language.
The user message is the AUGMENTED RAG prompt containing real context from the database.
The reference answer from pgvector grounds the LLM — it cannot hallucinate what a good
answer looks like because it is shown exactly what one is.
Format instructions make parsing reliable — split on "IMPROVED ANSWER:" always works.
response.choices[0].message.content extracts the text from the API response object.

---

## 13. app/api/routes/evaluate.py — Every Line Explained

### Written Mode Endpoint

```python
@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest, db: Session = Depends(get_db)):
```
POST endpoint. request — FastAPI validates JSON body against EvaluationRequest.
db — FastAPI calls get_db, takes the yielded session, passes it here.

```python
    user_embedding = get_embedding(request.user_answer)
```
Convert user's answer text to 384-dimensional vector.

```python
    reference = db.query(ReferenceAnswer)\
        .order_by(ReferenceAnswer.embedding.cosine_distance(user_embedding))\
        .first()
```
pgvector similarity search. ORDER BY cosine_distance sorts by how similar each stored
embedding is to the user's embedding — closest first. .first() returns the best match.
This is semantic search — finds the right reference even if question is worded differently.

```python
    similarity_score = compute_similarity(reference.embedding, user_embedding)
    covered = [c for c in reference.key_concepts if c.lower() in request.user_answer.lower()]
    missing = [c for c in reference.key_concepts if c.lower() not in request.user_answer.lower()]
    concept_score = (len(covered) / len(reference.key_concepts)) * 100 if reference.key_concepts else 0
    score = round((similarity_score * 0.5) + (concept_score * 0.5), 2)
```
Raw cosine similarity 0-100. List comprehensions check if each concept phrase appears
in the user's answer (case insensitive). Concept coverage percentage. Weighted final
score — 50% similarity + 50% concept coverage.

```python
    question = db.query(Question).filter(Question.id == reference.question_id).first()
```
Fetch question text for the RAG prompt.

```python
    if not missing:
        suggestions = "Great answer! You covered all the key concepts."
        improved_answer = "Your answer is already strong. Keep it concise and confident."
    else:
        bullet_points = "\n".join([f"• {concept}" for concept in missing])
        suggestions = f"Your answer was missing these key points:\n{bullet_points}"
        feedback = generate_feedback(
            question=question.text,
            user_answer=request.user_answer,
            reference_answer=reference.answer,
            missing_concepts=missing,
            score=similarity_score
        )
        improved_answer = ""
        if "IMPROVED ANSWER:" in feedback:
            parts = feedback.split("IMPROVED ANSWER:")
            improved_answer = parts[1].strip()
        else:
            improved_answer = feedback
```
If nothing missing — skip LLM entirely, return clean message.
If missing — generate suggestions in Python (100% accurate, no hallucination).
LLM only used for improved answer generation. Split on "IMPROVED ANSWER:" to extract
the text reliably.

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
    return EvaluationResponse(...)
```
Save evaluation to database. db.refresh() gets auto-generated id and created_at.
Return typed response — FastAPI validates and converts to JSON.

### MCQ Mode Endpoint

```python
@router.post("/evaluate/mcq", response_model=MCQResponse)
def evaluate_mcq(request: MCQRequest, db: Session = Depends(get_db)):
    reference = db.query(ReferenceAnswer)\
        .filter(ReferenceAnswer.question_id == request.question_id)\
        .first()
```
Filter by exact question_id — not similarity search. MCQ needs exact options for
the specific question selected.

```python
    correct_answer = reference.options[0]
    is_correct = request.selected_option == correct_answer
```
options[0] is always the correct answer in the stored data. Shuffling happens only
on the frontend display side. Simple string equality check — no ML needed.

```python
    if is_correct:
        explanation = f"Correct! {correct_answer}"
    else:
        explanation = f"Not quite. The correct answer is: {correct_answer}"
    return MCQResponse(
        correct=is_correct,
        selected_option=request.selected_option,
        correct_answer=correct_answer,
        explanation=explanation
    )
```
Return result with the correct answer revealed regardless of whether user was right.

---

## 14. app/api/routes/questions.py — Every Line Explained

```python
@router.get("/questions", response_model=list[QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions
```
SELECT * FROM questions. FastAPI maps each Question object to QuestionResponse
automatically using field names. list[QuestionResponse] validates each item.

```python
@router.get("/history/{question_id}", response_model=list[HistoryResponse])
def get_history(question_id: int, db: Session = Depends(get_db)):
    history = db.query(Evaluation).filter(Evaluation.question_id == question_id).all()
    return history
```
{question_id} in the path is a URL parameter. FastAPI extracts it automatically and
converts to int. Filter returns only evaluations for that specific question.

```python
@router.get("/questions/options/{question_id}")
def get_options(question_id: int, db: Session = Depends(get_db)):
    reference = db.query(ReferenceAnswer)\
        .filter(ReferenceAnswer.question_id == question_id)\
        .first()
    if not reference or not reference.options:
        return {"options": []}
    return {"options": reference.options}
```
Returns the 4 MCQ options for a specific question. Frontend calls this when user
selects a question in MCQ mode. Returns empty list if options not found.

---

## 15. Database Design

### Three Tables and Why

questions — stores each question once.
reference_answers — linked to questions via foreign key. Stores the correct answer,
key concepts, embedding, and MCQ options.
evaluations — linked to questions via foreign key. Stores every user submission with
full results and timestamp.

One big table would repeat question and reference data for every evaluation. Three
normalized tables follow proper relational database design.

### Foreign Keys

PostgreSQL enforces referential integrity. You cannot insert a reference_answer with
a question_id that does not exist. You cannot delete a question that has linked records.
This prevents orphaned data automatically.

### Why JSON for Lists

key_concepts, covered_concepts, missing_concepts, options are all lists of strings.
PostgreSQL JSON type stores them natively with automatic list-to-database conversion.

### Why Vector(384)

MiniLM always outputs 384-dimensional vectors. The column dimension must match exactly.
pgvector stores these and enables cosine distance search directly in SQL.

### Why server_default=func.now()

PostgreSQL sets the timestamp using the database server's time. More reliable than
Python-side datetime which depends on the application server's timezone and clock.

---

## 16. The ML Pipeline

```
User submits answer
        ↓
get_embedding(user_answer)
MiniLM → [0.25, -0.79, 0.41, ...] (384 numbers)
        ↓
pgvector: ORDER BY embedding <=> user_embedding
Finds closest reference answer in database
        ↓
compute_similarity(ref_embedding, user_embedding)
float(cosine_similarity result) * 100 = 87.12
        ↓
Concept detection:
[c for c in key_concepts if c.lower() in user_answer.lower()]
covered = [...], missing = [...]
        ↓
Weighted score:
(87.12 * 0.5) + (concept_coverage_pct * 0.5) = final_score
```

Why weighted scoring: pure cosine similarity inflated scores for short vague answers.
A one-line answer about overfitting scores ~86% on similarity alone because it mentions
the topic. With weighted scoring, zero concept coverage pulls the score to ~43%.

---

## 17. The RAG Pipeline

Retrieval Augmented Generation. Solves LLM hallucination.

Without RAG: send answer to LLM, LLM guesses what a good answer looks like. Generic,
possibly wrong, not grounded in your data.

With RAG:
R — Retrieve correct reference answer from database using pgvector
A — Augment the LLM prompt with that reference, missing concepts, and score
G — Generate feedback grounded in your specific data

The LLM sees the exact correct answer. It cannot hallucinate because it is shown exactly
what a good answer looks like.

Why built manually without LangChain: every step is understood and explainable.
In an interview you can trace through the exact code. LangChain would abstract this
into a black box you cannot explain.

---

# PART 2 — UPGRADES AND IMPROVEMENTS

---

## 18. Why We Made Changes

After building the initial system and testing it with real answers, several important
problems were identified through observation:

1. Improved answers were multi-paragraph essays — not interview style
2. Key concepts used academic jargon nobody says in real interviews
3. LLM was hallucinating suggestions about concepts the user already covered
4. Pure cosine similarity was inflating scores for short vague answers
5. Only 10 questions across 4 domains was insufficient for real practice
6. No MCQ mode — only written evaluation
7. Questions always appeared in the same order

Every fix was motivated by a real observed problem, not theoretical improvement.
This is good engineering practice — observe, diagnose, fix.

---

## 19. Fix 1 — Improved Answer Length and Tone

### Problem
LLM generated 3-4 paragraph essays. Example before fix:
"Overfitting occurs when a model learns the training data to the extent that it
negatively impacts performance on new unseen data due to high variance and poor
generalization capabilities, resulting in overly complex decision boundaries that
fail to capture the underlying distribution..."

This sounds like a textbook. Nobody speaks like this in an interview.

### What Changed
Updated the prompt in `app/core/rag.py` with:
- Explicit rules: exactly 3 sentences, simple everyday words
- A concrete bad example showing academic language
- A concrete good example showing interview-style language
- Instruction: "the way someone would actually speak out loud"

### Why Examples in Prompts Work
Telling the LLM "be concise" is vague — it interprets concise differently each time.
Showing a bad example and a good example gives a concrete target. LLMs follow examples
much more reliably than abstract instructions.

### Result After Fix
"Overfitting is when a model memorizes the training data too well including the noise
so it fails on new data. It performs well on training but poorly on test data.
You can prevent it using regularization, cross-validation, and early stopping."

3 sentences. Conversational. Interview-ready.

---

## 20. Fix 2 — Conversational Key Concepts

### Problem
Key concepts were academic single words:
```python
["generalization", "noise", "variance", "model complexity"]
```
Someone saying "the model fails on new data" would not match "generalization".
Someone saying "it memorizes the training data" would not match "noise".
Good answers were being penalized for using natural language.

### What Changed
Rewrote every concept in seed.py to use phrases people actually say:
```python
# Before — academic jargon
["generalization", "noise", "training data"]

# After — natural speech
["fails on new data", "memorizes training data", "performs well on training"]
```

Two rules applied:
1. Use phrases not single words — "fails on new data" matches spoken language
2. Include synonyms — multiple ways people say the same thing

### Why This Matters
Concept detection uses Python string matching. If concepts are phrases people actually
say, the system detects correct answers that were previously missed. Accuracy improved
significantly across all domains.

### Required Reseeding
Any time reference answers or concepts change, you must reseed. The embeddings in the
database must match the current content. Stale embeddings cause wrong pgvector matches.
```sql
TRUNCATE TABLE evaluations, reference_answers, questions RESTART IDENTITY CASCADE;
```
```bash
python seed.py
```

---

## 21. Fix 3 — Python-Generated Suggestions

### Problem
The LLM was generating suggestions about concepts the user had already covered.
Example: User said "poorly on test data" — it appeared in covered_concepts — but
the LLM suggested "You forgot to mention poor test performance."

The LLM was reading the reference answer and inventing its own list of missing things
instead of strictly using the missing_concepts list we provided.

### Root Cause
LLMs do not follow instructions with 100% reliability. Even with "IMPORTANT: only
address Missing Concepts listed above" — the LLM would occasionally look at the
reference answer and generate suggestions based on what it thought was missing.

### What Changed
Removed LLM from suggestions entirely. Suggestions now generated in Python:

```python
bullet_points = "\n".join([f"• {concept}" for concept in missing])
suggestions = f"Your answer was missing these key points:\n{bullet_points}"
```

LLM only used for the improved answer where natural language generation is needed.

### Why Python Cannot Hallucinate
Python executes exactly what you tell it. If missing = ["regularization", "early stopping"],
the output is exactly those two concepts. No invention. No assumptions. 100% accurate.

### What the LLM Now Does
Only generates the improved answer — a 3-sentence response that naturally incorporates
the missing concepts. This is what LLMs are genuinely good at: natural language
generation, not structured fact checking.

---

## 22. Fix 4 — Weighted Scoring

### Problem
Pure cosine similarity inflated scores for short vague answers.
"Supervised learning is a type of machine learning where model learns from data"
scored 86/100 despite covering zero key concepts.

### Root Cause
Cosine similarity measures semantic closeness, not completeness. A sentence that
begins with "Supervised learning is a type of machine learning" is very close to
the reference answer's opening — the embedding captures this high similarity even
though all important content is missing.

### What Changed
```python
# Before
score = compute_similarity(reference.embedding, user_embedding)

# After
similarity_score = compute_similarity(reference.embedding, user_embedding)
concept_score = (len(covered) / len(reference.key_concepts)) * 100
score = round((similarity_score * 0.5) + (concept_score * 0.5), 2)
```

50% semantic similarity + 50% concept coverage.

### Result
Same vague one-sentence answer: 86 → 18. Accurate.
Strong answer covering most concepts: 90. Also accurate.

### Why 50/50 Split
Semantic similarity captures overall understanding of the topic.
Concept coverage captures specific technical depth.
Equal weighting balances both — neither alone is sufficient.

---

## 23. New Feature — Difficulty Column

### What Was Added
A difficulty column to the questions table with values easy, medium, or hard.

### How It Was Added
1. Added to Question model in models.py:
```python
difficulty = Column(String, nullable=False, server_default="easy")
```
2. Generated migration:
```bash
alembic revision --autogenerate -m "add difficulty column to questions"
alembic upgrade head
```
3. Updated seed.py to include difficulty for each question

### Why server_default="easy"
Existing questions in the database before this migration needed a default value.
server_default tells PostgreSQL what to use for existing rows. Without this, the
migration would fail because nullable=False requires every row to have a value.

### Why Added Now
Prepares the database for adaptive difficulty — a future feature that serves harder
questions as user performance improves. The column and data are ready. Only the
logic needs to be built.

---

## 24. New Feature — 40 Questions Across 7 Domains

### What Was Added
Expanded from 10 questions in 4 domains to 40 questions in 7 domains.

New domains added:
- Python — directly relevant to internship and junior developer interviews
- Databases — tested in almost every backend interview
- Statistics — tested in ML and data science interviews

### What Makes These Questions Good

Reference answers: written in interview style — concise, direct, 3-5 sentences.
Not textbook paragraphs.

Key concepts: phrases people actually say in interviews. Not academic single words.

MCQ options: wrong options contain common misconceptions about the topic. They are
plausible enough to trick someone who does not know the concept but clearly wrong
to someone who does. All options are similar in length — no obvious "this is too
short to be right" giveaway.

Difficulty distribution:
Easy — foundational concepts every developer should know
Medium — concepts requiring understanding not just memorization
Hard — nuanced topics that require deeper knowledge

---

## 25. New Feature — Random Question Order

### What Was Added
Questions shuffle into a different order every time the page loads.

### Where Changed
Frontend only — index.html. Added Fisher-Yates shuffle:

```javascript
for (let i = data.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [data[i], data[j]] = [data[j], data[i]];
}
```

### What Fisher-Yates Is
The standard algorithm for randomly shuffling an array. Goes backwards through the
array, swapping each element with a randomly chosen element before it. Produces
a genuinely uniform random order. Named after Ronald Fisher and Frank Yates.

### Why This Matters
Without shuffling users always see the same questions first and only practice those.
With shuffling every session feels different and users naturally encounter diverse
questions across all domains.

### No Backend Changes Needed
The API returns all questions in the same order every time. Shuffling happens on the
client side. This is the right architecture — the server does not need to know or care
about display order.

---

## 26. New Feature — MCQ Mode (Full Explanation)

This was the most significant addition. Every component explained.

### What Was Added to the Database

options column in reference_answers:
```python
options = Column(JSON, nullable=True)
```
Stores 4 options per question as a JSON array. Index 0 is always the correct answer.
nullable=True because it was added after the table existed — existing rows have NULL.

Migration:
```bash
alembic revision --autogenerate -m "add options column to reference_answers"
alembic upgrade head
```

### How Options Are Designed

Correct answer (index 0): A concise accurate answer in interview style.

Wrong options (indexes 1, 2, 3): Each contains a common misconception.
- Wrong option 1: Usually reverses the concept (e.g. "FIFO" for a stack which is LIFO)
- Wrong option 2: Adds an incorrect constraint (e.g. "only works for classification")
- Wrong option 3: Completely wrong but sounds technical and plausible

All options are similar in length. No option is obviously wrong from its length alone.

### Why Index 0 Is Always Correct

Storing the correct answer at a fixed index makes backend checking a single line:
```python
correct_answer = reference.options[0]
is_correct = request.selected_option == correct_answer
```
The frontend shuffles display order randomly so users never see a pattern.
The backend does not need to know the shuffled order.

### What Was Added to the Backend

New schemas in schemas/evaluation.py:
```python
class MCQRequest(BaseModel):
    question_id: int
    selected_option: str
```
Uses question_id not question text. MCQ needs exact options for a specific question.
Text similarity search could potentially match the wrong question.

```python
class MCQResponse(BaseModel):
    correct: bool
    selected_option: str
    correct_answer: str
    explanation: str
```

New endpoint POST /evaluate/mcq in evaluate.py:
1. Takes question_id and selected_option
2. Fetches reference_answer filtered by exact question_id (not similarity search)
3. Compares selected_option to options[0]
4. Returns correct/incorrect with explanation

New endpoint GET /questions/options/{question_id} in questions.py:
Frontend calls this when a question is selected in MCQ mode.
Returns the 4 options for that specific question.
Frontend shuffles these before displaying.

### What Was Added to the Frontend

Mode toggle buttons:
```html
<button class="mode-btn active" onclick="setMode('written')">Written Mode</button>
<button class="mode-btn" onclick="setMode('mcq')">MCQ Mode</button>
```

setMode() function:
Shows/hides the textarea and options container based on selected mode.
If MCQ mode and a question is already selected, loads options immediately.

loadMCQOptions() function:
Calls GET /questions/options/{id}.
Passes options to renderOptions().

renderOptions() function:
Shuffles the 4 options using Fisher-Yates before displaying.
Creates a styled radio button label for each option.
Adds click handler to highlight the selected option visually.

submitMCQ() function:
Gets the selected radio button value.
Sends POST /evaluate/mcq with question_id and selected_option.
Calls showMCQResults() with the response.

showMCQResults() function:
Shows green checkmark and "Correct!" for correct answers.
Shows red X and "Not quite!" for wrong answers.
Reveals the correct answer in a blue box below regardless of result.

### Why question_id for MCQ but question text for Written

Written mode: pgvector searches by semantic similarity. The question text is embedded
and compared against stored question embeddings to find the right reference answer.
Different wording still matches the right question.

MCQ mode: we need exact options for a specific question. Using text similarity could
potentially return options for a slightly different question. question_id guarantees
we get options for exactly the right question.

### How Options Are Shuffled on Frontend

```javascript
const shuffled = [...options];  // copy the array, do not mutate original
for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
}
```

Spread operator [...options] creates a copy — original array unchanged.
Fisher-Yates shuffle produces random order.
Every page load and every question change shows options in different positions.

---

## 27. New Feature — Updated Frontend

### Complete Rewrite

The original frontend was minimal HTML. The new frontend was rewritten to support
two distinct modes while keeping the same simplicity principle.

### Mode State Management

```javascript
let currentMode = 'written';
let allQuestions = [];
let currentQuestionId = null;
```

Three global variables track state. currentMode determines which submit function runs.
currentQuestionId is set when user selects a question — used by MCQ mode to load options.

### Question Dropdown with Mode Awareness

```javascript
document.getElementById('questionSelect').addEventListener('change', function() {
    const selectedId = parseInt(this.value);
    if (!selectedId) return;
    currentQuestionId = selectedId;
    if (currentMode === 'mcq') loadMCQOptions(selectedId);
});
```

When question changes, updates currentQuestionId. If in MCQ mode, immediately loads
options for the new question. Written mode does not need this — it uses question text.

### data-text Attribute for Written Mode

```html
<option value="${q.id}" data-text="${q.text}">[${q.domain}] ${q.text}</option>
```

Each option stores both the id (for MCQ) and the text (for written mode) in the HTML.
Written mode retrieves the text with: `select.options[select.selectedIndex].dataset.text`

This lets the same dropdown serve both modes without making different API calls.

---

# PART 3 — REFERENCE

---

## 28. Every Error We Faced and How We Fixed It

### Error 1: pgvector Extension Not Available
```
ERROR: extension "vector" is not available
HINT: The extension must first be installed on the system
```
pgvector is not in standard PostgreSQL. Local PostgreSQL 18 on Windows did not have it.
Python's pip install pgvector and PostgreSQL's pgvector extension are two different
things — the Python package teaches SQLAlchemy about Vector types but does not install
the PostgreSQL extension.
Fix: Docker with pre-built pgvector/pgvector:pg16 image.

### Error 2: Password Authentication Failed (occurred twice)
```
FATAL: password authentication failed for user "postgres"
```
Local PostgreSQL running on port 5432 intercepted connections before Docker.
Fix: Stop local PostgreSQL via services.msc. Set startup type to Manual.
Diagnostic: netstat -ano | findstr :5432 shows what is using port 5432.

### Error 3: pgvector Not Defined in Migration File
```
NameError: name 'pgvector' is not defined
sa.Column('embedding', pgvector.sqlalchemy.vector.VECTOR(dim=384)...
```
Alembic autogenerate wrote the Vector column but did not import pgvector.
Fix: Manually add to migration file:
```python
from pgvector.sqlalchemy import Vector
# Change column to:
sa.Column('embedding', Vector(384), nullable=False)
```

### Error 4: numpy float64 Type Error
```
psycopg2.errors.InvalidSchemaName: schema "np" does not exist
LINE 1: ...score', np.float64(87.12)...
```
scikit-learn returns numpy float64. PostgreSQL does not understand numpy types.
Fix: float(score) in similarity.py converts to plain Python float.

### Error 5: FastAPI App Not Found
```
ERROR: Error loading ASGI app. Attribute "app" not found in module "app.main"
```
main.py was empty or not saved before running uvicorn.
Fix: Ensure code is saved. Run uvicorn app.main:app --reload from project root.

### Error 6: Swagger UI Showing Old Schema
Fields added to Pydantic schemas not appearing in API response or Swagger UI.
Python cached old compiled bytecode in __pycache__ folders.
Fix: Clear cache and restart.
```powershell
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
```
Diagnostic: Check http://localhost:8000/openapi.json for your field names.

### Error 7: CORS Blocking Frontend
Opening index.html as file:// URL blocked all API calls.
Fix: Serve index.html through FastAPI using FileResponse. Add CORSMiddleware.

### Error 8: JavaScript evaluate() Name Conflict
```
Uncaught TypeError: Failed to execute 'evaluate' on 'Document': 2 arguments required
```
document.evaluate() is a built-in browser method. Our function named evaluate()
conflicted with it.
Fix: Renamed to submitAnswer().

### Error 9: Score Inflated for Incomplete Answers
One-sentence vague answer scoring 86/100.
Root cause: Pure cosine similarity measures semantic closeness not completeness.
Fix: Weighted scoring combining similarity (50%) and concept coverage (50%).

### Error 10: Wrong Question Being Evaluated
User submitted supervised learning answer, system evaluated overfitting.
Root cause: Stale embeddings in database after rewriting reference answers.
Old embeddings no longer matched updated content so pgvector found wrong match.
Fix: TRUNCATE all tables, reseed with fresh embeddings.

### Error 11: LLM Hallucinating Suggestions
LLM suggested things the user had already said.
Root cause: LLMs do not follow instructions with 100% reliability even with
explicit "IMPORTANT: only address Missing Concepts" instruction.
Fix: Remove LLM from suggestions entirely. Generate in Python from missing list.

### Error 12: Concept Tags Running Together
Covered and missing concept tags appeared with no spacing between them.
Root cause: JavaScript .join('') joins with nothing. CSS margin was too small.
Fix: margin: 3px 4px in CSS. innerHTML with .replace(/\n/g, '<br>') for line breaks.

### Error 13: Docker Not Running After Computer Restart
Container stops when computer shuts down.
Not an error but a common confusion. Fix: docker start pgvector-db every session.
Set local PostgreSQL startup type to Manual to prevent port conflicts on boot.

---

## 29. Interview Questions — What If Scenarios

**What if the user asks a question not in the database?**
pgvector still returns the closest reference answer. But evaluation quality degrades if
the submitted question is completely different from anything stored. Proper fix: check
similarity between submitted question and stored questions. If below 0.5 threshold,
generate reference dynamically via LLM and cache it.

**What if the LLM generates a bad improved answer?**
The else branch in parsing puts everything in improved_answer. Score and concepts are
still computed correctly in Python — those never depend on the LLM. The evaluation is
never completely broken even if LLM output is poor.

**What if two users evaluate simultaneously?**
FastAPI handles concurrent requests. Each gets its own session from get_db. SQLAlchemy
manages connection pooling. PostgreSQL uses row-level locking. No data corruption.

**What if the Groq API is down?**
Currently returns 500 error. Production fix: try/except around generate_feedback with
fallback message. Score and concepts still return even when LLM fails.

**What if concept detection misses a concept because user used synonyms?**
Known limitation. Current detection is keyword-based. "The model performs badly on
unseen examples" would not match "fails on new data". Fix: embedding-based concept
detection — compare concept embeddings against answer segments. Noted as future improvement.

**What if the database grows to 100,000 questions?**
Add HNSW index for logarithmic search:
```sql
CREATE INDEX ON reference_answers USING hnsw (embedding vector_cosine_ops);
```
pgvector handles millions of vectors with proper indexing.

**What if a user wants to track progress over time?**
evaluations table already stores all attempts with timestamps and scores. GET /history
already returns this data. Progress chart just needs to visualize it — backend is ready.

---

## 30. Interview Questions — Why Not This Instead

**Why not LangChain?**
Building RAG manually means every step is understood and explainable. LangChain
abstracts retrieval and prompt construction into black boxes. "I built the RAG pipeline
manually" is a strong signal in an interview. You can trace through every line of code.

**Why not OpenAI embeddings?**
Free. Local. No API cost per call. Development generates hundreds of embedding calls.
MiniLM's 384-dim embeddings are sufficient for our semantic similarity use case. User
data never leaves the machine.

**Why not Pinecone?**
For hundreds of questions pgvector in PostgreSQL is simpler and free. Pinecone adds a
separate paid service, separate API keys, and external network latency. Add dedicated
vector database only when you have millions of vectors at high concurrency.

**Why not Flask?**
Flask requires manual request parsing, separate validation library, separate docs library,
no async by default. FastAPI gives all of this automatically. For ML APIs FastAPI is
the modern industry standard.

**Why not MongoDB?**
Our data is relational — questions have reference answers, evaluations link to questions.
PostgreSQL models this naturally with foreign keys. MongoDB would require manual
relationship management and does not support pgvector.

**Why not JWT authentication?**
Deprioritized to keep focus on the ML and RAG components — the core technical value.
Adding auth requires users table, register/login endpoints, token management, protected
routes. Clearly noted as a future improvement.

**Why not LLM for suggestions?**
The LLM was hallucinating. Python-generated suggestions from the exact missing concepts
list are 100% accurate. Use the right tool for each job — Python for structured fact
checking, LLM for natural language generation.

---

## 31. How to Start the Project Every Time

```bash
# 1. Navigate to project
cd path/to/interview-evaluator

# 2. Activate virtual environment
venv\Scripts\activate
# Confirm (venv) appears in terminal

# 3. Start Docker container
docker start pgvector-db
# If Docker Desktop is not open, open it first and wait for "Engine running"

# 4. Start the API
uvicorn app.main:app --reload
# Wait for: INFO: Application startup complete.

# 5. Open
# Web Interface: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Troubleshooting

**Password authentication failed:**
Local PostgreSQL is running on port 5432.
Open services.msc → find PostgreSQL → Stop.

**Schema changes not reflected:**
```powershell
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
```
Restart uvicorn.

**Questions not loading in frontend:**
Check Docker is running: docker ps
Check browser console (F12) for error messages.

**After changing database models:**
```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

**To clear all data and reseed:**
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

**To push changes to GitHub:**
```bash
git add .
git commit -m "describe your changes"
git push
```

---


*Complete documentation for the AI-Powered Interview Preparation System*
*Built by Moiz Nisar*
*FastAPI · PostgreSQL · pgvector · sentence-transformers · Groq LLaMA 3*
