from typing import Literal

from pydantic import BaseModel, Field


class StoryGenerateRequest(BaseModel):
    mode: Literal["generate", "provided"] = Field(
        ...,
        description="generate = Gemini creates the story, provided = user supplies the story",
    )

    prompt: str | None = Field(
        default=None,
        min_length=10,
        description="Story idea when mode is generate.",
    )

    story: str | None = Field(
        default=None,
        min_length=10,
        description="Complete story when mode is provided.",
    )

    duration_minutes: float = Field(
        default=5.0,
        ge=1.0,
        le=30.0,
        description="Target narration duration in minutes.",
    )

    voice: Literal[
        "af_heart",
        "am_adam",
    ] = Field(
        default="af_heart",
        description="Kokoro voice.",
    )

    speed: float = Field(
        default=1.0,
        ge=0.7,
        le=1.3,
        description="Global narration speed.",
    )


class StoryGenerateResponse(BaseModel):
    message: str
    filename: str