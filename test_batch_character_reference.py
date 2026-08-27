from app.services.story_analyzer import StoryAnalyzer
from app.services.visual_bible_service import VisualBibleService
from app.services.image.batch_character_reference_service import (
    BatchCharacterReferenceService,
)


STORY = """
Arun is a young man who lives in a poor rural village.

One evening, Arun discovers an old letter hidden inside
his family's house. The letter contains a mysterious
message about his father's disappearance.

Arun decides to investigate the truth and begins his
journey the following morning.
"""


def main() -> None:

    print("=" * 70)
    print("STEP 1: ANALYZING STORY")
    print("=" * 70)

    analysis = StoryAnalyzer().analyze_story(STORY)

    print(
        f"Title: {analysis.title}"
    )

    print(
        f"Scenes: {len(analysis.scenes)}"
    )

    print()
    print("=" * 70)
    print("STEP 2: CREATING VISUAL BIBLE")
    print("=" * 70)

    visual_bible = (
        VisualBibleService()
        .create_visual_bible(analysis)
    )

    print(
        f"Characters: {len(visual_bible.characters)}"
    )

    for character in visual_bible.characters:
        print(
            f"- {character.name}"
        )

    print()
    print("=" * 70)
    print("STEP 3: GENERATING CHARACTER REFERENCES")
    print("=" * 70)

    service = BatchCharacterReferenceService()

    generated_images = service.generate_all(
        visual_bible=visual_bible
    )

    print()
    print("=" * 70)
    print("CHARACTER REFERENCES GENERATED")
    print("=" * 70)

    for image_path in generated_images:
        print(
            f"- {image_path}"
        )

    print("=" * 70)


if __name__ == "__main__":
    main()

