from typing import Literal

from pydantic import BaseModel, Field


# ============================================================
# Common Visual Attribute
# ============================================================


class VisualAttribute(BaseModel):
    value: str

    source: Literal[
        "story",
        "creative",
    ]


# ============================================================
# Character Visual Identity
# ============================================================


class CharacterVisual(BaseModel):
    name: str

    # Original story information
    story_description: str

    # Visual identity
    age: VisualAttribute | None = None
    gender: VisualAttribute | None = None
    physical_appearance: VisualAttribute | None = None
    hair: VisualAttribute | None = None
    face: VisualAttribute | None = None
    skin_tone: VisualAttribute | None = None
    body_build: VisualAttribute | None = None

    # Clothing and accessories
    clothing: VisualAttribute | None = None
    accessories: list[VisualAttribute] = Field(
        default_factory=list
    )

    # Stable visual identifiers
    distinctive_features: list[VisualAttribute] = Field(
        default_factory=list
    )

    # Behaviour / expression guidance
    expression_guidance: list[str] = Field(
        default_factory=list
    )

    # Rules that must remain consistent across images
    consistency_notes: list[str] = Field(
        default_factory=list
    )


# ============================================================
# Location / World Identity
# ============================================================


class LocationVisual(BaseModel):
    name: str

    story_description: str

    visual_description: VisualAttribute | None = None

    architecture: VisualAttribute | None = None
    environment: VisualAttribute | None = None
    terrain: VisualAttribute | None = None

    consistency_notes: list[str] = Field(
        default_factory=list
    )


# ============================================================
# Important Object Identity
# ============================================================


class ObjectVisual(BaseModel):
    name: str

    story_description: str

    visual_description: VisualAttribute | None = None

    material: VisualAttribute | None = None
    shape: VisualAttribute | None = None
    condition: VisualAttribute | None = None

    distinctive_features: list[VisualAttribute] = Field(
        default_factory=list
    )

    consistency_notes: list[str] = Field(
        default_factory=list
    )


# ============================================================
# Global 2D Illustration Style
# ============================================================


class VisualStyle(BaseModel):

    # Global style identity
    style: VisualAttribute

    # Mandatory illustration direction
    medium: VisualAttribute

    rendering: VisualAttribute | None = None

    # Lighting and atmosphere
    lighting: VisualAttribute | None = None
    color_mood: VisualAttribute | None = None
    atmosphere: VisualAttribute | None = None

    # Cinematic language
    cinematic_direction: VisualAttribute | None = None

    # Global rules applied to every image
    consistency_notes: list[str] = Field(
        default_factory=list
    )


# ============================================================
# Visual Bible
# ============================================================


class VisualBible(BaseModel):

    characters: list[CharacterVisual] = Field(
        default_factory=list
    )

    locations: list[LocationVisual] = Field(
        default_factory=list
    )

    important_objects: list[ObjectVisual] = Field(
        default_factory=list
    )

    visual_style: VisualStyle
