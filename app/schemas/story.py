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

    language: Literal[
        "en",
        "hi",
        "fr",
    ] = Field(
        default="en",
        description="Narration language.",
    )

    voice: Literal[
        "af_heart",
        "af_bella",
        "af_sarah",
        "af_nicole",
        "af_sky",
        "am_adam",
        "hf_alpha",
        "hf_beta",
        "hm_omega",
        "hm_psi",
        "ff_siwis",
    ] = Field(
        default="af_heart",
        description="Kokoro voice ID.",
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
