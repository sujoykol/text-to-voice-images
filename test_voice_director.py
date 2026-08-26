from app.schemas.narration import NarrationSegment
from app.services.voice_director import VoiceDirector


segment = NarrationSegment(
    segment=1,
    text="Govind discovered that the butter weighed only 900 grams.",
    emotion="dramatic",
    intensity=0.8,
    pace="slow",
    pause_before=0.8,
    pause_after=1.2,
    emphasis=["900 grams"],
)


director = VoiceDirector()

parameters = director.direct(segment)

print(parameters)
