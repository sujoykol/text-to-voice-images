from pathlib import Path

from app.services.audio_converter import AudioConverter


converter = AudioConverter()

input_file = Path("audio/story.wav")
output_file = Path("audio/story.mp3")

result = converter.wav_to_mp3(
    input_file,
    output_file,
)

print(f"Generated: {result}")
