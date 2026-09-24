
from pathlib import Path

from app.schemas.character_reference import CharacterReference
from app.schemas.image_prompt import ImagePrompt
from app.services.image.cloudflare_image_provider import (
    CloudflareImageProvider,
)


class CharacterReferenceImageService:

    REFERENCE_DIR = Path("images/references")

    def __init__(self) -> None:
        self.provider = CloudflareImageProvider()

        self.REFERENCE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def generate(
        self,
        character_reference: CharacterReference,
    ) -> Path:

        if character_reference is None:
            raise ValueError(
                "character reference is required"
            )

        if not character_reference.reference_prompt.strip():
            raise ValueError(
                "character reference prompt cannot be empty"
            )

        image_prompt = ImagePrompt(
            scene_number=0,
            prompt=character_reference.reference_prompt,
            characters=[],
            location=None,
            important_objects=[],
            visual_style=(
                "Bright 2D vector-style Indian moral/story illustration, "
                "clean controlled outlines, "
                "clean flat vector-style shapes, "
                "simple readable character forms, "
                "expressive natural facial features, "
                "recognizable silhouette, "
                "consistent stylized body proportions, "
                "vibrant harmonious colors, "
                "clean flat color regions, "
                "simple vector-style shading, "
                "authentic Indian clothing where appropriate, "
                "consistent character construction, "
                "polished illustrated storytelling aesthetic. "
                "No photorealism, no 3D rendering, "
                "no photography, no painterly textures, "
                "no digital painting, no anime styling."
            ),
            cinematography={
                "shot_type": "full-body character reference",
                "camera_angle": "eye level",
                "composition": (
                    "centered character with full body visible"
                ),
                "depth": "clean simple background",
                "visual_focus": "character identity",
            },
            continuity_instructions=[
                "Maintain the same character identity.",
                "Maintain stable facial features.",
                "Maintain stable hairstyle.",
                "Maintain stable body proportions.",
                "Maintain stable clothing.",
                "Do not turn the reference into a story scene.",
            ],
        )

        output_path = (
            self.REFERENCE_DIR
            / f"{character_reference.name.lower().replace(' ', '_')}_reference.jpg"
        )

        return self.provider.generate(
            image_prompt=image_prompt,
            output_path=output_path,
        )
