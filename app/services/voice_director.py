from dataclasses import dataclass

from app.schemas.narration import NarrationSegment


@dataclass(frozen=True)
class VoiceParameters:
    speed: float
    volume: float
    pause_before: float
    pause_after: float
    emphasis: list[str]


class VoiceDirector:
    """
    Converts narration instructions into practical
    voice-generation parameters.
    """

    def direct(self, segment: NarrationSegment) -> VoiceParameters:
        speed = self._calculate_speed(
            segment.pace,
            segment.emotion,
            segment.intensity,
        )

        volume = self._calculate_volume(
            segment.emotion,
            segment.intensity,
        )

        pause_before = segment.pause_before
        pause_after = segment.pause_after

        return VoiceParameters(
            speed=speed,
            volume=volume,
            pause_before=pause_before,
            pause_after=pause_after,
            emphasis=segment.emphasis,
        )

    @staticmethod
    def _calculate_speed(
        pace: str,
        emotion: str,
        intensity: float,
    ) -> float:

        pace_speeds = {
            "very_slow": 0.75,
            "slow": 0.88,
            "normal": 1.00,
            "fast": 1.12,
            "very_fast": 1.25,
        }

        speed = pace_speeds.get(pace, 1.0)

        # Emotional adjustments
        if emotion == "suspense":
            speed -= 0.03 * intensity

        elif emotion == "dramatic":
            speed -= 0.04 * intensity

        elif emotion == "reflective":
            speed -= 0.05 * intensity

        elif emotion == "happy":
            speed += 0.03 * intensity

        return max(0.70, min(speed, 1.30))

    @staticmethod
    def _calculate_volume(
        emotion: str,
        intensity: float,
    ) -> float:

        volume = 1.0

        if emotion == "suspense":
            volume -= 0.05 * intensity

        elif emotion == "dramatic":
            volume += 0.05 * intensity

        elif emotion == "happy":
            volume += 0.03 * intensity

        elif emotion == "reflective":
            volume -= 0.03 * intensity

        return max(0.8, min(volume, 1.2))
