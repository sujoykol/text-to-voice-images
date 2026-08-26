from pathlib import Path

import soundfile as sf

from app.schemas.narration import NarrationSegment
from app.services.voice_director import VoiceDirector


class TTSService:

    def __init__(
        self,
        voice: str = "af_heart",
        lang_code: str = "a",
        speed: float = 1.0,
    ) -> None:

        from kokoro import KPipeline

        self.pipeline = KPipeline(
            lang_code=lang_code
        )

        self.voice_director = VoiceDirector()

        self.voice = voice
        self.speed = speed

        self.output_dir = Path("audio/temp")
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def generate_segment(
        self,
        segment: NarrationSegment,
    ) -> Path:

        parameters = self.voice_director.direct(
            segment
        )

        output_path = (
            self.output_dir
            / f"segment_{segment.segment:03d}.wav"
        )

        final_speed = (
            parameters.speed * self.speed
        )

        generator = self.pipeline(
            segment.text,
            voice=self.voice,
            speed=final_speed,
        )

        for _, _, audio in generator:

            sf.write(
                output_path,
                audio,
                24000,
            )

            break

        print(
            f"Segment {segment.segment}: "
            f"voice={self.voice}, "
            f"emotion={segment.emotion}, "
            f"speed={final_speed:.2f}, "
            f"volume={parameters.volume:.2f}"
        )

        return output_path