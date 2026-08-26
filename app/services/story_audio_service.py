from pathlib import Path

from app.services.audio_converter import AudioConverter
from app.services.audio_renderer import AudioRenderer
from app.services.narration_director import NarrationDirector
from app.services.story_writer import StoryWriter
from app.services.tts_service import TTSService
from app.utils.filename import safe_filename


class StoryAudioService:

    def __init__(self) -> None:
        self.story_writer = StoryWriter()
        self.narration_director = NarrationDirector()
        self.audio_renderer = AudioRenderer()
        self.audio_converter = AudioConverter()

        self.audio_dir = Path("audio")
        self.audio_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.temp_dir = self.audio_dir / "temp"
        self.temp_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def generate_story_audio(
        self,
        mode: str,
        prompt: str | None = None,
        story: str | None = None,
        duration_minutes: float = 5.0,
        output_name: str | None = None,
        voice: str = "af_heart",
        speed: float = 1.0,
    ) -> Path:

        # -----------------------------
        # 1. Obtain the story
        # -----------------------------

        if mode == "generate":

            if not prompt:
                raise ValueError(
                    "prompt is required when mode='generate'"
                )

            print("Generating story with Gemini...")

            final_story = self.story_writer.generate_story(
                prompt,
                duration_minutes=duration_minutes,
            )

        elif mode == "provided":

            if not story:
                raise ValueError(
                    "story is required when mode='provided'"
                )

            print("Using user-provided story...")

            final_story = story

        else:

            raise ValueError(
                "mode must be 'generate' or 'provided'"
            )

        print(
            f"Story length: {len(final_story)} characters"
        )

        # -----------------------------
        # 2. Create narration plan
        # -----------------------------

        narration_plan = (
            self.narration_director
            .create_narration_plan(final_story)
        )

        print(
            f"Narration plan: "
            f"{len(narration_plan.segments)} segments"
        )

        # -----------------------------
        # 3. Configure TTS
        # -----------------------------

        tts_service = TTSService(
            voice=voice,
            speed=speed,
        )

        rendered_segments = []

        for segment in narration_plan.segments:

            audio_path = (
                tts_service
                .generate_segment(segment)
            )

            rendered_segments.append(
                (
                    audio_path,
                    segment.pause_before,
                    segment.pause_after,
                )
            )

        # -----------------------------
        # 4. Determine final filename
        # -----------------------------

        if output_name is None:

            filename_source = (
                prompt
                if mode == "generate"
                else story
            )

            output_name = safe_filename(
                filename_source or "story"
            )

        # -----------------------------
        # 5. Render temporary WAV
        # -----------------------------

        wav_path = self.audio_dir / "story.wav"

        self.audio_renderer.render(
            rendered_segments,
            wav_path,
        )

        # -----------------------------
        # 6. Convert WAV → MP3
        # -----------------------------

        mp3_path = self.audio_dir / output_name

        self.audio_converter.wav_to_mp3(
            wav_path,
            mp3_path,
        )

        # -----------------------------
        # 7. Cleanup temporary files
        # -----------------------------

        for audio_path, _, _ in rendered_segments:

            if audio_path.exists():
                audio_path.unlink()

        if wav_path.exists():
            wav_path.unlink()

        print(
            f"Final audio generated: {mp3_path}"
        )

        return mp3_path