from pydantic import BaseModel, Field


class CharacterReference(BaseModel):
    name: str

    reference_prompt: str

    age: str | None = None

    gender: str | None = None

    physical_appearance: str | None = None

    hair: str | None = None

    face: str | None = None

    skin_tone: str | None = None

    body_build: str | None = None

    clothing: str | None = None

    distinctive_features: list[str] = Field(
        default_factory=list
    )

    consistency_notes: list[str] = Field(
        default_factory=list
    )
