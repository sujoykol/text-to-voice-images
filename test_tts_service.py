from app.services.tts_service import TTSService
from app.schemas.narration import NarrationSegment


segment = NarrationSegment(
    segment=1,
    text="In a small village in India, a clever shopkeeper named Govind ran a modest shop.",
    emotion="neutral",
    intensity=0.2,
    pace="normal",
    pause_before=0.0,
    pause_after=0.5,
    emphasis=["Govind"],
)

tts = TTSService()

output = tts.generate_segment(segment)

print(f"Generated: {output}")
