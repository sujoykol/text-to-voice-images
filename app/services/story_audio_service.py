from pathlib import Path

from app.config.tts import LANGUAGE_CONFIG
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
        language: str = "en",
    ) -> Path:

        # -----------------------------------------
        # 0. Validate language and voice
        # -----------------------------------------

        print(
            f"DEBUG -> language={language!r}, voice={voice!r}"
        )

        language_config = LANGUAGE_CONFIG.get(language)
        #language_config = self.LANGUAGE_CONFIG.get(language)

        if language_config is None:
            raise ValueError(
                f"Unsupported narration language: {language}"
            )

        if voice not in language_config["voices"]:
            raise ValueError(
                f"Voice '{voice}' is not available "
                f"for language '{language}'"
            )

        lang_code = language_config["lang_code"]

        print(
            f"Narration language: "
            f"{language_config['name']} "
            f"(Kokoro: {lang_code})"
        )

        print(
            f"Narration voice: {voice}"
        )

        # -----------------------------------------
        # 1. Obtain the story
        # -----------------------------------------

        if mode == "generate":

            if not prompt or not prompt.strip():
                raise ValueError(
                    "prompt is required when mode='generate'"
                )

            print(
                "Generating story with Gemini..."
            )

            final_story = (
                self.story_writer.generate_story(
                    prompt.strip(),
                    duration_minutes=duration_minutes,
                )
            )

        elif mode == "provided":

            if not story or not story.strip():
                raise ValueError(
                    "story is required when mode='provided'"
                )

            print(
                "Using user-provided story..."
            )

            final_story = story.strip()

        else:

            raise ValueError(
                "mode must be 'generate' or 'provided'"
            )

        print(
            f"Story length: "
            f"{len(final_story)} characters"
        )

        # -----------------------------------------
        # 2. Create narration plan
        # -----------------------------------------

        print(
            "Creating narration plan..."
        )

        narration_plan = (
            self.narration_director
            .create_narration_plan(
                final_story
            )
        )

        print(
            f"Narration plan: "
            f"{len(narration_plan.segments)} segments"
        )

        # -----------------------------------------
        # 3. Configure TTS
        # -----------------------------------------

        tts_service = TTSService(
            voice=voice,
            lang_code=lang_code,
            speed=speed,
        )

        rendered_segments = []

        # -----------------------------------------
        # 4. Generate narration segments
        # -----------------------------------------

        for segment in narration_plan.segments:

            print(
                f"Generating audio segment "
                f"{segment.segment}/"
                f"{len(narration_plan.segments)}..."
            )

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

        # -----------------------------------------
        # 5. Determine final filename
        # -----------------------------------------

        if output_name is None:

            filename_source = (
                prompt
                if mode == "generate"
                else story
            )

            output_name = safe_filename(
                filename_source or "story"
            )

        # -----------------------------------------
        # 6. Render WAV
        # -----------------------------------------

        wav_path = (
            self.audio_dir / "story.wav"
        )

        print(
            "Rendering final WAV..."
        )

        self.audio_renderer.render(
            rendered_segments,
            wav_path,
        )

        # -----------------------------------------
        # 7. Convert WAV → MP3
        # -----------------------------------------

        mp3_path = (
            self.audio_dir / output_name
        )

        print(
            "Converting WAV → MP3..."
        )

        self.audio_converter.wav_to_mp3(
            wav_path,
            mp3_path,
        )

        # -----------------------------------------
        # 8. Cleanup temporary files
        # -----------------------------------------

        for audio_path, _, _ in rendered_segments:

            if audio_path.exists():
                audio_path.unlink()

        if wav_path.exists():
            wav_path.unlink()

        # -----------------------------------------
        # 9. Final result
        # -----------------------------------------

        print(
            f"Final audio generated: {mp3_path}"
        )

        return mp3_path
