from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.story import router as story_router


app = FastAPI(
    title="Voice Story AI",
    description="AI-powered story narration and voice generation.",
    version="0.1.0",
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# API ROUTES
# ==================================================

app.include_router(story_router)


# ==================================================
# ROOT
# ==================================================

@app.get("/")
def root():
    return {
        "message": "Voice Story AI API is running"
    }


# ==================================================
# HEALTH
# ==================================================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }