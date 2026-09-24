from pathlib import Path

from app.schemas.character_reference import CharacterReference
from app.schemas.image_prompt import ImagePrompt
from app.services.image.cloudflare_image_provider import (
    CloudflareImageProvider,
)


def main() -> None:

    reference = CharacterReference(
        name="Sujoy",
        reference_prompt=(
            "Full-body character reference illustration of Sujoy, "
            "a young man from a poor village, standing upright "
            "in a neutral pose and facing forward. "
            "Show the complete character from head to toe. "
            "Clear readable face, clear hairstyle, stable body "
            "proportions, unobstructed silhouette, neutral "
            "expression, simple clean background. "
            "Bright 2D vector-style Indian moral/story illustration, clean controlled outlines, clean flat vector-style shapes, simple readable character forms, expressive natural facial features, vibrant harmonious colors, simple vector-style shading, authentic Indian clothing, polished illustrated storytelling aesthetic."
            "not a story scene."
        ),
    )

    image_prompt = ImagePrompt(
        scene_number=0,
        prompt=reference.reference_prompt,
        characters=[],
        location=None,
        important_objects=[],
        visual_style=(
            "Bright 2D vector-style Indian moral/story illustration, "
            "clean controlled outlines, clean flat vector-style shapes, "
            "simple readable character forms, expressive natural facial "
            "features, vibrant harmonious colors, simple vector-style shading, "
            "authentic Indian clothing, polished illustrated storytelling aesthetic."
        ),
        cinematography={
            "shot_type": "full-body character reference",
            "camera_angle": "eye level",
            "composition": "centered character, full body visible",
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

    provider = CloudflareImageProvider()

    output_path = Path(
        "images/references/sujoy_reference.jpg"
    )

    result = provider.generate(
        image_prompt=image_prompt,
        output_path=output_path,
    )

    print()
    print("=" * 70)
    print("CHARACTER REFERENCE GENERATED")
    print("=" * 70)
    print(f"Character : {reference.name}")
    print(f"Output    : {result}")
    print("=" * 70)


if __name__ == "__main__":
    main()
