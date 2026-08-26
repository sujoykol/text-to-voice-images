from pathlib import Path

from app.services.audio_renderer import AudioRenderer


renderer = AudioRenderer()

segments = [
    (
        Path("audio/segment_001.wav"),
        0.0,
        1.0,
    ),
    (
        Path("audio/segment_001.wav"),
        0.8,
        1.5,
    ),
]

output = renderer.render(
    segments,
    Path("audio/story_test.wav"),
)

print(f"Generated: {output}")
