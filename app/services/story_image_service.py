from pathlib import Path

from app.services.batch_scene_prompt_service import (
    BatchScenePromptService,
)
from app.services.image.batch_character_reference_service import (
    BatchCharacterReferenceService,
)
from app.services.image.image_generation_service import (
    ImageGenerationService,
)
from app.services.story_analyzer import StoryAnalyzer
from app.services.visual_bible_service import VisualBibleService
from app.utils.filename import safe_folder_name


class StoryImageService:

    def __init__(self) -> None:

        self.story_analyzer = StoryAnalyzer()

        self.visual_bible_service = (
            VisualBibleService()
        )

        self.batch_character_reference_service = (
            BatchCharacterReferenceService()
        )

        self.batch_scene_prompt_service = (
            BatchScenePromptService()
        )

        self.image_generation_service = (
            ImageGenerationService()
        )

        self.image_root = Path("images")

        self.image_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def generate_story_images(
        self,
        story: str,
        image_count: int,
    ) -> list[Path]:

        # ==================================================
        # 1. Validate input
        # ==================================================

        if not story or not story.strip():
            raise ValueError(
                "story cannot be empty"
            )

        if image_count < 1:
            raise ValueError(
                "image count must be greater than zero"
            )

        # ==================================================
        # 2. Analyze story
        # ==================================================

        print()
        print("=" * 70)
        print("STEP 1: ANALYZING STORY")
        print("=" * 70)

        analysis = (
            self.story_analyzer.analyze_story(
                story=story.strip(),
                target_scene_count=image_count,
            )
        )

        print(
            f"Title: {analysis.title}"
        )

        print(
            f"Scenes: {len(analysis.scenes)}"
        )

        # ==================================================
        # 3. Create visual bible
        # ==================================================

        print()
        print("=" * 70)
        print("STEP 2: CREATING VISUAL BIBLE")
        print("=" * 70)

        visual_bible = (
            self.visual_bible_service
            .create_visual_bible(
                analysis
            )
        )

        print(
            f"Characters: "
            f"{len(visual_bible.characters)}"
        )

        for character in visual_bible.characters:
            print(
                f"- {character.name}"
            )

        # ==================================================
        # 4. Create story directory
        # ==================================================

        story_folder = safe_folder_name(
            analysis.title
        )

        output_dir = (
            self.image_root / story_folder
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ==================================================
        # 5. Generate character references
        # ==================================================

        print()
        print("=" * 70)
        print("STEP 3: GENERATING CHARACTER REFERENCES")
        print("=" * 70)

        character_reference_images = (
            self.batch_character_reference_service
            .generate_all(
                visual_bible=visual_bible
            )
        )

        print()
        print(
            f"Generated "
            f"{len(character_reference_images)} "
            f"character reference image(s)."
        )

        # ==================================================
        # 6. Create scene prompts
        # ==================================================

        print()
        print("=" * 70)
        print("STEP 4: CREATING SCENE PROMPTS")
        print("=" * 70)

        prompt_batch = (
            self.batch_scene_prompt_service
            .create_all_prompts(
                analysis=analysis,
                visual_bible=visual_bible,
            )
        )

        print(
            f"Created "
            f"{len(prompt_batch.prompts)} "
            f"scene image prompts."
        )

        # ==================================================
        # 7. Generate scene images
        # ==================================================

        print()
        print("=" * 70)
        print("STEP 5: GENERATING SCENE IMAGES")
        print("=" * 70)

        generated_images: list[Path] = []

        for index, image_prompt in enumerate(
            prompt_batch.prompts,
            start=1,
        ):

            scene_number = (
                image_prompt.scene_number
            )

            output_path = (
                output_dir
                / f"{scene_number}.jpg"
            )

            print(
                f"Generating scene "
                f"{index}/{len(prompt_batch.prompts)}..."
            )

            generated_path = (
                self.image_generation_service
                .generate_scene_image(
                    image_prompt=image_prompt,
                    output_path=output_path,
                )
            )

            generated_images.append(
                generated_path
            )

            print(
                f"Generated: {generated_path}"
            )

        # ==================================================
        # 8. Final result
        # ==================================================

        print()
        print("=" * 70)
        print("STORY IMAGE GENERATION COMPLETE")
        print("=" * 70)

        print(
            f"Character references: "
            f"{len(character_reference_images)}"
        )

        print(
            f"Scene images: "
            f"{len(generated_images)}"
        )

        print(
            f"Output directory: "
            f"{output_dir}"
        )

        print("=" * 70)

        return generated_images
