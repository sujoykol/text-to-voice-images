from pathlib import Path

from app.schemas.image_prompt import ImagePrompt
from app.services.image.cloudflare_image_provider import (
    CloudflareImageProvider,
)


class SceneImageService:

    SCENE_DIR = Path("images/scenes")

    def __init__(self) -> None:
        self.provider = CloudflareImageProvider()

        self.SCENE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def generate(
        self,
        image_prompt: ImagePrompt,
        reference_images: list[Path] | None = None,
    ) -> Path:

        # --------------------------------------------------
        # Validate prompt
        # --------------------------------------------------

        if image_prompt is None:
            raise ValueError(
                "image prompt is required"
            )

        if not image_prompt.prompt.strip():
            raise ValueError(
                "image prompt cannot be empty"
            )

        # --------------------------------------------------
        # Normalize reference images
        # --------------------------------------------------

        if reference_images is None:
            reference_images = []

        if len(reference_images) > 4:
            raise ValueError(
                "maximum 4 reference images are supported"
            )

        # --------------------------------------------------
        # Validate reference images
        # --------------------------------------------------

        for reference_image in reference_images:

            if not reference_image.exists():
                raise FileNotFoundError(
                    f"reference image not found: "
                    f"{reference_image}"
                )

            if not reference_image.is_file():
                raise ValueError(
                    f"reference image is not a file: "
                    f"{reference_image}"
                )

        # --------------------------------------------------
        # Output path
        # --------------------------------------------------

        output_path = (
            self.SCENE_DIR
            / f"scene_{image_prompt.scene_number:03d}.jpg"
        )

        # --------------------------------------------------
        # Generate image
        # --------------------------------------------------

        return self.provider.generate(
            image_prompt=image_prompt,
            output_path=output_path,
            reference_images=reference_images,
        )
