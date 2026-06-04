# 🎯 AI-Powered Interview Preparation System

> A full-stack AI system that helps developers prepare for technical interviews using semantic evaluation, concept detection, and LLM-generated feedback.

Built by **Moiz Nisar** | Python · FastAPI · PostgreSQL · pgvector · RAG · LLaMA 3

---

## What It Does

Submit a technical interview answer and the system:

1. Converts your answer to a **vector embedding** using MiniLM
2. Searches a **PostgreSQL + pgvector** database for the closest reference answer
3. Computes a **weighted score** — 50% semantic similarity + 50% concept coverage
4. Detects exactly which **key concepts** you covered and which you missed
5. Generates a **concise improved answer** using LLaMA 3 via Groq (RAG pipeline)
6. Saves every evaluation for **progress tracking**

Or switch to **MCQ Mode** — pick from 4 shuffled options and get instant feedback.

---

## Demo

**Written Mode**
```
Question: What is overfitting and how can you prevent it?
Answer:   Overfitting is when the model does well on training but fails on test data.

Score:    43 / 100
Covered:  performs well on training · poorly on test data
Missing:  memorizes training data · regularization · cross-validation · early stopping

Suggestions:
• memorizes training data
• regularization
• cross-validation
• early stopping

Improved Answer:
Overfitting is when a model memorizes the training data too well including the noise
so it fails on new data. It performs well on training but poorly on test data.
You can prevent it using regularization, cross-validation, and early stopping.
```

**MCQ Mode**
```
Question: What is a primary key?

(A) Uniquely identifies each row, cannot be null, gets automatic index
(B) A label for the table that does not have to be unique
(C) Optional metadata stored alongside each row
(D) A backup copy of the foreign key in the same table

Selected: (A) → ✅ Correct!
```

---

## Architecture

```
User Answer (text)
        │
        ▼
┌─────────────────────┐
│  MiniLM Embeddings  │  sentence-transformers
│  384-dim vector     │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  pgvector Search    │  PostgreSQL + pgvector
│  cosine distance    │  ← RETRIEVAL (R in RAG)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Weighted Scoring   │  sklearn cosine similarity
│  Concept Detection  │  Python string matching
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  RAG Prompt Builder │  ← AUGMENTED (A in RAG)
│  + Groq LLM         │  ← GENERATION (G in RAG)
└─────────────────────┘
        │
        ▼
   Final Response:
   Score · Concepts · Suggestions · Improved Answer
```

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| API Framework | FastAPI | Auto Swagger UI, Pydantic validation, async support |
| Database | PostgreSQL + pgvector | Vector storage alongside relational data in one place |
| ORM + Migrations | SQLAlchemy + Alembic | Type-safe queries, versioned schema changes |
| Embeddings | sentence-transformers (MiniLM) | Free, local, 384-dim, no API cost |
| Similarity | scikit-learn | cosine_similarity in one line |
| LLM | LLaMA 3 via Groq API | Free tier, sub-second inference |
| Containerization | Docker | pgvector pre-installed, zero configuration |
| Frontend | HTML + JavaScript | Simple, clean, no framework dependencies |

---

## Scoring System

```
Final Score = (Semantic Similarity × 0.5) + (Concept Coverage × 0.5)

Semantic Similarity = cosine_similarity(user_embedding, reference_embedding) × 100
Concept Coverage    = (covered_concepts / total_concepts) × 100
```

**Why weighted scoring?**
Pure cosine similarity inflates scores for short vague answers. A one-sentence answer
about a topic scores around 85% on similarity because it mentions the right words but
covers zero key concepts. The weighted approach correctly penalizes incomplete answers.

| Score | Rating |
|---|---|
| 75 – 100 | Strong Answer |
| 45 – 74 | Decent Answer |
| 0 – 44 | Needs Work |

---

## Question Bank

**40 questions across 7 domains with 3 difficulty levels**

| Domain | Questions | Difficulties |
|---|---|---|
| Machine Learning | 6 | Easy · Medium |
| Deep Learning | 5 | Easy · Medium · Hard |
| DSA | 6 | Easy · Medium · Hard |
| System Design | 6 | Easy · Medium |
| Python | 7 | Easy · Medium |
| Databases | 5 | Easy · Medium |
| Statistics | 5 | Easy · Medium · Hard |

Each question has a reference answer written in interview style, conversational key
concepts that match how people actually speak, and 4 MCQ options with one correct
and three plausible but wrong answers.

---

## Two Evaluation Modes

**Written Mode** — Type a free-form answer. The system evaluates it semantically,
detects which concepts you covered and missed, generates Python-based suggestions
from the exact missing concepts, and produces a concise LLM-generated improved answer.

**MCQ Mode** — Select from 4 shuffled options. The system checks your selection
against the stored correct answer and returns correct or incorrect with the correct
answer revealed.

---

## Project Structure

```
interview-evaluator/
├── app/
│   ├── api/routes/
│   │   ├── evaluate.py       # POST /evaluate, POST /evaluate/mcq
│   │   └── questions.py      # GET /questions, /history, /options
│   ├── core/
│   │   ├── embeddings.py     # MiniLM embedding generation
│   │   ├── similarity.py     # Weighted cosine similarity scoring
│   │   └── rag.py            # RAG pipeline + Groq LLM
│   ├── db/
│   │   ├── models.py         # SQLAlchemy models (3 tables)
│   │   └── session.py        # DB connection, Base, get_db dependency
│   ├── schemas/
│   │   └── evaluation.py     # Pydantic request/response models
│   └── main.py               # FastAPI app, CORS middleware, routers
├── alembic/                  # Database migration files
├── seed.py                   # Populates DB with 40 questions and embeddings
├── index.html                # Web frontend (Written + MCQ modes)
├── requirements.txt
└── .env                      # Environment variables (not committed)
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/evaluate` | Evaluate a written answer |
| `POST` | `/evaluate/mcq` | Evaluate an MCQ selection |
| `GET` | `/questions` | List all 40 questions |
| `GET` | `/questions/options/{id}` | Get MCQ options for a question |
| `GET` | `/history/{question_id}` | Get evaluation history |
| `GET` | `/` | Web interface |
| `GET` | `/docs` | Swagger UI |

### POST /evaluate — Example

Request:
```json
{
  "question": "What is overfitting and how can you prevent it?",
  "user_answer": "Overfitting is when the model performs well on training data but poorly on test data."
}
```

Response:
```json
{
  "question_id": 2,
  "score": 43.06,
  "covered_concepts": ["performs well on training", "poorly on test data"],
  "missing_concepts": ["memorizes training data", "regularization", "cross-validation", "early stopping"],
  "suggestions": "Your answer was missing these key points:\n• memorizes training data\n• regularization\n• cross-validation\n• early stopping",
  "improved_answer": "Overfitting is when a model memorizes the training data too well including the noise so it fails on new data. It performs well on training but poorly on test data. You can prevent it using regularization, cross-validation, and early stopping."
}
```

### POST /evaluate/mcq — Example

Request:
```json
{
  "question_id": 1,
  "selected_option": "Supervised learning uses labelled data where each example has an input and an expected output"
}
```

Response:
```json
{
  "correct": true,
  "selected_option": "Supervised learning uses labelled data...",
  "correct_answer": "Supervised learning uses labelled data...",
  "explanation": "Correct! Supervised learning uses labelled data where each example has an input and an expected output"
}
```

---

## Database Schema

```
questions
├── id              INTEGER PRIMARY KEY (auto-increment)
├── text            VARCHAR NOT NULL
├── domain          VARCHAR NOT NULL
└── difficulty      VARCHAR NOT NULL DEFAULT 'easy'

reference_answers
├── id              INTEGER PRIMARY KEY
├── question_id     INTEGER FK → questions.id
├── answer          VARCHAR NOT NULL
├── key_concepts    JSON NOT NULL
├── embedding       VECTOR(384) NOT NULL
└── options         JSON (index 0 is always the correct MCQ answer)

evaluations
├── id              INTEGER PRIMARY KEY
├── question_id     INTEGER FK → questions.id
├── user_answer     VARCHAR NOT NULL
├── score           FLOAT NOT NULL
├── covered_concepts JSON NOT NULL
├── missing_concepts JSON NOT NULL
├── suggestions     VARCHAR NOT NULL
├── improved_answer VARCHAR NOT NULL
└── created_at      TIMESTAMPTZ server default NOW()
```

---

## Setup Guide

### Prerequisites
- Python 3.10+
- Docker Desktop

### 1. Clone
```bash
git clone https://github.com/moiznisar/interview-evaluator.git
cd interview-evaluator
```

### 2. Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL + pgvector
```bash
docker run --name pgvector-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=interview_evaluator \
  -p 5432:5432 \
  -d pgvector/pgvector:pg16
```

### 5. Create .env File
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/interview_evaluator
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
```

Get a free Groq API key at https://console.groq.com

### 6. Run Migrations
```bash
alembic upgrade head
```

### 7. Seed Database
```bash
python seed.py
```

Downloads MiniLM on first run (~90MB), generates embeddings for all 40 reference
answers, and populates the database.

### 8. Start
```bash
uvicorn app.main:app --reload
```

- Web Interface → http://localhost:8000
- API Docs → http://localhost:8000/docs

### Every Session
```bash
docker start pgvector-db
venv\Scripts\activate
uvicorn app.main:app --reload
```

---

## Key Technical Decisions

**Why RAG built manually instead of LangChain?**
Building the retrieval, prompt construction, and response parsing manually means every
step is understood and explainable. LangChain abstracts these into black boxes. For a
portfolio project, understanding the internals is more valuable than convenience.

**Why pgvector instead of Pinecone?**
For hundreds of questions, keeping vectors in the same PostgreSQL database as relational
data is simpler, cheaper (free), and faster (no external network calls). Dedicated vector
databases make sense at millions of vectors with very high concurrency.

**Why weighted scoring instead of pure cosine similarity?**
Pure similarity inflates scores for short vague answers. Combining semantic similarity
(50%) with concept coverage (50%) produces scores that reflect actual answer quality.

**Why Python-generated suggestions instead of LLM?**
The LLM was hallucinating suggestions about concepts the user had already covered.
Python-generated suggestions from the exact missing concepts list are 100% accurate.
The LLM is only used for generating the improved answer where natural language
generation is genuinely needed.

**Why conversational key concepts instead of academic terms?**
Users speak naturally. "The model fails on new data" is how someone would answer in
an interview, not "poor generalization to unseen data distributions." Matching concepts
against natural speech significantly improves detection accuracy.

---

## Improvements Made After Initial Build

After real-world testing, several important issues were identified and fixed:

- Improved answer reduced from multi-paragraph essays to 3 concise interview-style sentences
- Key concepts rewritten from academic jargon to natural conversational phrases
- Suggestions moved from LLM to Python to eliminate hallucination
- Weighted scoring introduced to fix inflated scores for vague short answers
- Question bank expanded from 10 to 40 questions across 7 domains
- MCQ mode added as a second evaluation mode with shuffled options
- Difficulty tags added to every question
- Random question shuffle on every page load

---

## Future Improvements

- Adaptive difficulty — serve harder questions as user performance improves
- Test session mode — timed 10-question tests with final score report
- Progress dashboard — score improvement chart over time per domain
- Audio input — speech-to-text for evaluating spoken answers
- User authentication — personal accounts with individual history
- Embedding-based concept detection — catch paraphrases and synonyms
- Expand to 100+ questions across more domains

---

## Author

**Moiz Nisar**
GitHub: [@moiznisar](https://github.com/moiznisar)

*Built with FastAPI · PostgreSQL · pgvector · sentence-transformers · Groq LLaMA 3*
