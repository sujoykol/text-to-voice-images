from pathlib import Path

from app.core.config import settings
from app.schemas.image_prompt import ImagePrompt
from app.services.image.cloudflare_image_provider import CloudflareImageProvider
from app.services.image.gemini_image_provider import GeminiImageProvider


class ImageGenerationService:

    IMAGE_DIR = Path("images")

    def __init__(self) -> None:

        if settings.IMAGE_PROVIDER == "cloudflare":
            self.provider = CloudflareImageProvider()

        elif settings.IMAGE_PROVIDER == "gemini":
            self.provider = GeminiImageProvider()

        else:
            raise ValueError(
                f"Unsupported image provider: "
                f"{settings.IMAGE_PROVIDER}"
            )

        self.IMAGE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def generate_scene_image(
        self,
        image_prompt: ImagePrompt,
        output_path: Path,
    ) -> Path:

        if image_prompt is None:
            raise ValueError(
                "image prompt is required"
            )

        if not image_prompt.prompt.strip():
            raise ValueError(
                "image prompt cannot be empty"
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        return self.provider.generate(
            image_prompt=image_prompt,
            output_path=output_path,
        )    

   