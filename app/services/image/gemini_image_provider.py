import base64
from pathlib import Path

from google import genai

from app.core.config import settings
from app.schemas.image_prompt import ImagePrompt
from app.services.image.provider import ImageProvider


class GeminiImageProvider(ImageProvider):

    MODEL_NAME = "gemini-3.1-flash-image"

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def generate(
        self,
        image_prompt: ImagePrompt,
        output_path: Path,
    ) -> Path:

        if image_prompt is None:
            raise ValueError(
                "image prompt is required"
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            interaction = self.client.interactions.create(
                model=self.MODEL_NAME,
                input=image_prompt.prompt,
                response_format={
                    "type": "image",
                    "mime_type": "image/jpeg",
                    "aspect_ratio": "16:9",
                    "image_size": "1K",
                },
            )

            if interaction.output_image is None:
                raise ValueError(
                    "Gemini returned no image"
                )

            image_bytes = base64.b64decode(
                interaction.output_image.data
            )

            output_path.write_bytes(
                image_bytes
            )

            return output_path

        except Exception as exc:
            raise RuntimeError(
                f"Gemini image generation failed: {exc}"
            ) from exc