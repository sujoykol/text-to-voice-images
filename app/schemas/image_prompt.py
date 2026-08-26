from pydantic import BaseModel, Field


# ============================================================
# Character Reference
# ============================================================


class CharacterPromptReference(BaseModel):
    name: str

    # Stable identity attributes
    age: str | None = None
    gender: str | None = None
    physical_appearance: str | None = None
    hair: str | None = None
    face: str | None = None
    skin_tone: str | None = None
    body_build: str | None = None

    # Stable clothing
    clothing: str | None = None

    # Stable recognition features
    distinctive_features: list[str] = Field(
        default_factory=list
    )

    # Continuity instructions
    consistency_notes: list[str] = Field(
        default_factory=list
    )


# ============================================================
# Cinematography
# ============================================================


class CinematographyDirection(BaseModel):
    shot_type: str

    camera_angle: str

    composition: str

    depth: str | None = None

    visual_focus: str | None = None


# ============================================================
# Image Prompt
# ============================================================


class ImagePrompt(BaseModel):

    # Scene identity
    scene_number: int

    # Final production prompt
    prompt: str

    # Persistent character references
    characters: list[CharacterPromptReference] = Field(
        default_factory=list
    )

    # Location identity
    location: str | None = None

    # Important objects visible in this scene
    important_objects: list[str] = Field(
        default_factory=list
    )

    # Global illustration language
    visual_style: str

    # Cinematic direction for this specific image
    cinematography: CinematographyDirection

    # Explicit continuity rules
    continuity_instructions: list[str] = Field(
        default_factory=list
    )
