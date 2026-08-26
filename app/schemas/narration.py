from enum import Enum

from pydantic import BaseModel, Field


class Emotion(str, Enum):
    PEACEFUL = "peaceful"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEARFUL = "fearful"
    SUSPENSE = "suspense"
    SURPRISE = "surprise"
    HOPEFUL = "hopeful"
    DRAMATIC = "dramatic"
    REFLECTIVE = "reflective"
    NEUTRAL = "neutral"


class Pace(str, Enum):
    VERY_SLOW = "very_slow"
    SLOW = "slow"
    NORMAL = "normal"
    FAST = "fast"
    VERY_FAST = "very_fast"


class NarrationSegment(BaseModel):
    segment: int = Field(ge=1)
    text: str = Field(min_length=1)
    emotion: Emotion
    intensity: float = Field(ge=0.0, le=1.0)
    pace: Pace
    pause_before: float = Field(ge=0.0, le=5.0)
    pause_after: float = Field(ge=0.0, le=5.0)
    emphasis: list[str] = Field(default_factory=list)

class NarrationPlan(BaseModel):
    segments: list[NarrationSegment] = Field(min_length=1)
