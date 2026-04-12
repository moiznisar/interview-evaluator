from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes.evaluate import router as evaluate_router
from app.api.routes.questions import router as questions_router

app = FastAPI(
    title="Interview Evaluator API",
    description="AI-powered interview answer evaluation system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(evaluate_router)
app.include_router(questions_router)

@app.get("/")
def root():
    return FileResponse("index.html")