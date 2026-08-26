from pydantic import BaseModel, Field


class StoryFact(BaseModel):
    category: str
    fact: str


class CharacterAnalysis(BaseModel):
    name: str
    role: str
    description: str
    personality: list[str] = Field(
        default_factory=list
    )


class SceneAnalysis(BaseModel):
    scene_number: int
    description: str
    location: str
    time: str
    mood: str
    characters: list[str] = Field(
        default_factory=list
    )
    visual_elements: list[str] = Field(
        default_factory=list
    )


class StoryAnalysis(BaseModel):
    title: str
    genre: str
    theme: str
    protagonist: str
    central_conflict: str

    facts: list[StoryFact] = Field(
        default_factory=list
    )

    characters: list[CharacterAnalysis] = Field(
        default_factory=list
    )

    setting: str

    emotional_arc: list[str] = Field(
        default_factory=list
    )

    key_events: list[str] = Field(
        default_factory=list
    )

    climax: str
    resolution: str
    conclusion_meaning: str

    scenes: list[SceneAnalysis] = Field(
        default_factory=list
    )


class StoryAnalysisRequest(BaseModel):
    story: str


class StoryImageGenerationRequest(BaseModel):
    story: str = Field(
        ...,
        min_length=10,
        description="Story to generate images from.",
    )

    image_count: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Number of story images to generate.",
    )