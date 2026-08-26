from fastapi import FastAPI

from app.api.story import router as story_router


app = FastAPI(
    title="Voice Story AI",
    description="AI-powered story narration and voice generation.",
    version="0.1.0",
)

app.include_router(story_router)


@app.get("/")
def root():
    return {
        "message": "Voice Story AI API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
