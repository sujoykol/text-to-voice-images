from pathlib import Path

import soundfile as sf
from kokoro import KPipeline


TEXT = (
    "In a small village in India, a clever shopkeeper named Govind "
    "ran a modest shop."
)

OUTPUT_DIR = Path("audio")
OUTPUT_DIR.mkdir(exist_ok=True)

pipeline = KPipeline(lang_code="a")

generator = pipeline(
    TEXT,
    voice="af_heart",
    speed=1.0,
)

for index, (_, _, audio) in enumerate(generator):
    output_path = OUTPUT_DIR / f"test_voice_{index + 1}.wav"
    sf.write(output_path, audio, 24000)
    print(f"Generated: {output_path}")
