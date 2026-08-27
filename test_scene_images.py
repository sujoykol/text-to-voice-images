from pathlib import Path

from app.services.story_analyzer import StoryAnalyzer
from app.services.visual_bible_service import VisualBibleService
from app.services.image.batch_character_reference_service import (
    BatchCharacterReferenceService,
)
from app.services.batch_scene_prompt_service import (
    BatchScenePromptService,
)
from app.services.image.scene_image_service import (
    SceneImageService,
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

    # ==================================================
    # STEP 1: STORY ANALYSIS
    # ==================================================

    print("=" * 70)
    print("STEP 1: ANALYZING STORY")
    print("=" * 70)

    analysis = StoryAnalyzer().analyze_story(STORY)

    print(f"Title : {analysis.title}")
    print(f"Scenes: {len(analysis.scenes)}")

    # ==================================================
    # STEP 2: VISUAL BIBLE
    # ==================================================

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
        print(f"- {character.name}")

    # ==================================================
    # STEP 3: CHARACTER REFERENCES
    # ==================================================

    print()
    print("=" * 70)
    print("STEP 3: GENERATING CHARACTER REFERENCES")
    print("=" * 70)

    character_reference_service = (
        BatchCharacterReferenceService()
    )

    character_reference_images = (
        character_reference_service.generate_all(
            visual_bible=visual_bible
        )
    )

    print()
    print("Character reference images:")

    for image_path in character_reference_images:
        print(f"- {image_path}")

    # ==================================================
    # STEP 4: SCENE PROMPTS
    # ==================================================

    print()
    print("=" * 70)
    print("STEP 4: GENERATING SCENE PROMPTS")
    print("=" * 70)

    scene_prompt_service = (
        BatchScenePromptService()
    )

    image_prompt_batch = (
        scene_prompt_service.create_all_prompts(
            analysis=analysis,
            visual_bible=visual_bible,
        )
    )

    print()
    print(
        f"Scene prompts generated: "
        f"{len(image_prompt_batch.prompts)}"
    )

    for prompt in image_prompt_batch.prompts:

        print()
        print(
            f"Scene {prompt.scene_number}"
        )
        print("-" * 70)
        print(prompt.prompt)

    # ==================================================
    # STEP 5: SCENE IMAGES
    # ==================================================

    print()
    print("=" * 70)
    print("STEP 5: GENERATING SCENE IMAGES")
    print("=" * 70)

    scene_image_service = SceneImageService()

    generated_scene_images: list[Path] = []

    for prompt in image_prompt_batch.prompts:

        print()
        print(
            f"Generating scene {prompt.scene_number}..."
        )

        # --------------------------------------------------
        # Character reference images
        #
        # For this V1 test there is one character reference.
        # The same reference is supplied to scenes containing
        # the character.
        # --------------------------------------------------

        reference_images = character_reference_images

        image_path = scene_image_service.generate(
            image_prompt=prompt,
            reference_images=reference_images,
        )

        generated_scene_images.append(
            image_path
        )

        print(
            f"Generated: {image_path}"
        )

    # ==================================================
    # FINAL RESULT
    # ==================================================

    print()
    print("=" * 70)
    print("SCENE IMAGE GENERATION COMPLETE")
    print("=" * 70)

    print()
    print("Character references:")

    for image_path in character_reference_images:
        print(f"- {image_path}")

    print()
    print("Scene images:")

    for image_path in generated_scene_images:
        print(f"- {image_path}")

    print()
    print("=" * 70)
    print("VOICE STORY AI V1 IMAGE PIPELINE TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
