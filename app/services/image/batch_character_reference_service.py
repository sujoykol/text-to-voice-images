from pathlib import Path

from app.schemas.visual_bible import VisualBible
from app.services.image.character_reference_service import (
    CharacterReferenceService,
)
from app.services.image.character_reference_image_service import (
    CharacterReferenceImageService,
)


class BatchCharacterReferenceService:

    def __init__(self) -> None:

        self.character_reference_service = (
            CharacterReferenceService()
        )

        self.character_reference_image_service = (
            CharacterReferenceImageService()
        )

    def generate_all(
        self,
        visual_bible: VisualBible,
    ) -> list[Path]:

        if visual_bible is None:
            raise ValueError(
                "visual bible is required"
            )

        if not visual_bible.characters:
            raise ValueError(
                "visual bible contains no characters"
            )

        generated_images: list[Path] = []

        visual_style = None

        if visual_bible.visual_style:
            visual_style = (
                visual_bible.visual_style.style.value
            )

        for character in visual_bible.characters:

            print()
            print(
                f"Generating character reference "
                f"for: {character.name}"
            )

            # -----------------------------------------
            # Create character reference definition
            # -----------------------------------------

            character_reference = (
                self.character_reference_service
                .create_reference(
                    character=character,
                    visual_style=visual_style,
                )
            )

            # -----------------------------------------
            # Generate reference image
            # -----------------------------------------

            image_path = (
                self.character_reference_image_service
                .generate(
                    character_reference=character_reference
                )
            )

            generated_images.append(image_path)

            print(
                f"Generated: {image_path}"
            )

        return generated_images
