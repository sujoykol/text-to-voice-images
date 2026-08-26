from pathlib import Path

import numpy as np
import soundfile as sf


class AudioRenderer:
    SAMPLE_RATE = 24000

    def render(
        self,
        audio_segments: list[tuple[Path, float, float]],
        output_path: Path,
    ) -> Path:
        """
        Combine speech segments with silence.

        Each tuple contains:
            (audio_path, pause_before, pause_after)
        """

        audio_parts: list[np.ndarray] = []

        for audio_path, pause_before, pause_after in audio_segments:

            if pause_before > 0:
                audio_parts.append(
                    self._silence(pause_before)
                )

            audio, sample_rate = sf.read(audio_path)

            if sample_rate != self.SAMPLE_RATE:
                raise ValueError(
                    f"Expected {self.SAMPLE_RATE} Hz audio, "
                    f"got {sample_rate} Hz"
                )

            audio_parts.append(audio)

            if pause_after > 0:
                audio_parts.append(
                    self._silence(pause_after)
                )

        if not audio_parts:
            raise ValueError("No audio segments provided.")

        final_audio = np.concatenate(audio_parts)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        sf.write(
            output_path,
            final_audio,
            self.SAMPLE_RATE,
        )

        return output_path

    def _silence(self, seconds: float) -> np.ndarray:
        samples = int(
            seconds * self.SAMPLE_RATE
        )

        return np.zeros(
            samples,
            dtype=np.float32,
        )
