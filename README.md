# 🎯 AI-Powered Interview Answer Evaluator

A hybrid **ML + RAG + LLM** system that evaluates technical interview answers using semantic similarity, concept detection, and AI-generated feedback.

Built by **Moiz Nisar** as a portfolio project demonstrating real-world AI system design.

---

## 🧠 What It Does

When a user submits a technical interview answer, the system:

1. Converts the answer into a **vector embedding** using MiniLM
2. Searches a **PostgreSQL + pgvector** database for the closest reference answer
3. Computes a **weighted similarity score** (50% semantic + 50% concept coverage)
4. Detects **covered and missing key concepts**
5. Sends everything to **LLaMA 3 via Groq** to generate improvement suggestions and a professional improved answer
6. Saves the evaluation to the database for **progress tracking**

---

## 🏗️ Architecture

```
User Answer (text)
        │
        ▼
┌─────────────────────┐
│  MiniLM Embeddings  │  sentence-transformers
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  pgvector Search    │  PostgreSQL + pgvector
│  (closest match)    │  Retrieval (R in RAG)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Cosine Similarity  │  sklearn
│  Concept Detection  │  ML Core
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  RAG Prompt Builder │  Augmented (A in RAG)
│  + Groq LLM         │  Generation (G in RAG)
└─────────────────────┘
        │
        ▼
   Final Response:
   Score + Concepts + Suggestions + Improved Answer
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| API Framework | FastAPI | REST API + Swagger UI |
| Database | PostgreSQL + pgvector | Store questions, embeddings, evaluations |
| ORM | SQLAlchemy + Alembic | Database models and migrations |
| Embeddings | sentence-transformers (MiniLM) | Convert text to vectors |
| Similarity | scikit-learn | Cosine similarity scoring |
| LLM | LLaMA 3 via Groq API | Generate feedback and improved answers |
| Containerization | Docker | Run PostgreSQL + pgvector |
| Frontend | HTML + JavaScript | Simple web interface |

---

## ✨ Features

- **Semantic Evaluation** — understands meaning, not just keyword matching
- **Weighted Scoring** — 50% semantic similarity + 50% concept coverage
- **Concept Detection** — identifies exactly what was covered and what was missed
- **RAG Pipeline** — LLM feedback grounded in reference data, no hallucination
- **Progress Tracking** — every evaluation saved with timestamp
- **REST API** — fully documented via Swagger UI at `/docs`
- **Web Interface** — simple frontend at `/`
- **Multi-domain** — supports ML, Deep Learning, DSA, and System Design questions

---

## 📁 Project Structure

```
interview-evaluator/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── evaluate.py      # POST /evaluate
│   │       └── questions.py     # GET /questions, GET /history
│   ├── core/
│   │   ├── embeddings.py        # MiniLM embedding generation
│   │   ├── similarity.py        # Cosine similarity scoring
│   │   └── rag.py               # RAG pipeline + Groq LLM
│   ├── db/
│   │   ├── models.py            # SQLAlchemy table definitions
│   │   └── session.py           # Database connection
│   ├── schemas/
│   │   └── evaluation.py        # Pydantic request/response models
│   └── main.py                  # FastAPI app entry point
├── alembic/                     # Database migrations
├── seed.py                      # Database seeding script
├── index.html                   # Web frontend
├── requirements.txt
└── .env                         # Environment variables (not pushed)
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- Docker Desktop

### 1. Clone the repository
```bash
git clone https://github.com/moiznisar/interview-evaluator.git
cd interview-evaluator
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL + pgvector with Docker
```bash
docker run --name pgvector-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=interview_evaluator \
  -p 5432:5432 \
  -d pgvector/pgvector:pg16
```

### 5. Create `.env` file
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/interview_evaluator
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
```

### 6. Run database migrations
```bash
alembic upgrade head
```

### 7. Seed the database
```bash
python seed.py
```

### 8. Start the API
```bash
uvicorn app.main:app --reload
```

### 9. Open the app
- **Web Interface** → http://localhost:8000
- **API Docs (Swagger UI)** → http://localhost:8000/docs

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/evaluate` | Evaluate an interview answer |
| `GET` | `/questions` | Get all available questions |
| `GET` | `/history/{question_id}` | Get evaluation history for a question |
| `GET` | `/` | Web interface |
| `GET` | `/docs` | Swagger UI documentation |

### Example Request
```json
POST /evaluate
{
    "question": "What is overfitting and how can you prevent it?",
    "user_answer": "Overfitting is when a model performs well on training data but poorly on test data."
}
```

### Example Response
```json
{
    "question_id": 2,
    "score": 43.06,
    "covered_concepts": ["training data"],
    "missing_concepts": ["noise", "generalization", "regularization", "cross-validation", "early stopping"],
    "suggestions": "1. Consider mentioning the role of noise in overfitting...",
    "improved_answer": "Overfitting occurs when a model learns the noise and details of training data..."
}
```

---

## 🗄️ Database Schema

```
questions
├── id (PK)
├── text
└── domain (ML / DL / DSA / System Design)

reference_answers
├── id (PK)
├── question_id (FK → questions)
├── answer
├── key_concepts (JSON)
└── embedding (Vector 384)

evaluations
├── id (PK)
├── question_id (FK → questions)
├── user_answer
├── score
├── covered_concepts (JSON)
├── missing_concepts (JSON)
├── suggestions
├── improved_answer
└── created_at
```

---

## 💡 Key Technical Decisions

**Why RAG instead of pure LLM?**
Without retrieval, the LLM would hallucinate what a "correct" answer looks like. RAG grounds the feedback in our specific reference database — consistent, accurate, and explainable.

**Why build RAG manually instead of LangChain?**
Building the retrieval and prompt construction manually gives full control and deeper understanding of the pipeline. Every line can be explained clearly.

**Why pgvector instead of a dedicated vector database?**
For this scale, keeping vectors in PostgreSQL alongside relational data is simpler, cheaper, and easier to maintain than running a separate vector database like Pinecone.

**Why weighted scoring?**
Pure cosine similarity inflates scores for short, vague answers that are semantically close but conceptually incomplete. Combining similarity (50%) with concept coverage (50%) produces more accurate and meaningful scores.

---

## 📊 Scoring System

```
Final Score = (Semantic Similarity × 0.5) + (Concept Coverage × 0.5)

Semantic Similarity = cosine_similarity(user_embedding, reference_embedding) × 100
Concept Coverage    = (covered_concepts / total_concepts) × 100
```

| Score Range | Rating |
|---|---|
| 75 – 100 | Strong Answer |
| 45 – 74 | Decent Answer |
| 0 – 44 | Needs Work |

---

## 🌱 Future Improvements

- Add audio input (speech-to-text) for spoken answers
- Domain-wise performance analytics
- User authentication and personal dashboards
- More question domains (Behavioral, System Design deep dives)
- Fine-tuned embedding model for technical interview domain

---

## 👤 Author

**Moiz Nisar**
- GitHub: [@moiznisar](https://github.com/moiznisar)

---

*Built with FastAPI, PostgreSQL, pgvector, sentence-transformers, and Groq LLaMA 3*
