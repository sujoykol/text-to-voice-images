from pathlib import Path

from app.services.batch_scene_prompt_service import (
    BatchScenePromptService,
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

        # -----------------------------------------
        # Validate input
        # -----------------------------------------

        if not story or not story.strip():
            raise ValueError(
                "story cannot be empty"
            )

        if image_count < 1:
            raise ValueError(
                "image count must be greater than zero"
            )

        # -----------------------------------------
        # 1. Analyze story
        # -----------------------------------------

        print("Analyzing story...")

        analysis = (
            self.story_analyzer.analyze_story(
                story=story.strip(),
                target_scene_count=image_count,
            )
        )

        print(
            f"Story analysis created "
            f"{len(analysis.scenes)} scenes."
        )

        # -----------------------------------------
        # 2. Create visual bible
        # -----------------------------------------

        print("Creating visual bible...")

        visual_bible = (
            self.visual_bible_service
            .create_visual_bible(
                analysis
            )
        )

        # -----------------------------------------
        # 3. Create scene prompts
        # -----------------------------------------

        print(
            "Creating scene image prompts..."
        )

        prompt_batch = (
            self.batch_scene_prompt_service
            .create_all_prompts(
                analysis=analysis,
                visual_bible=visual_bible,
            )
        )

        print(
            f"Created {len(prompt_batch.prompts)} "
            f"image prompts."
        )

        # -----------------------------------------
        # 4. Create story directory
        # -----------------------------------------

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

        # -----------------------------------------
        # 5. Generate images
        # -----------------------------------------

        generated_images: list[Path] = []

        for image_prompt in prompt_batch.prompts:

            scene_number = (
                image_prompt.scene_number
            )

            output_path = (
                output_dir
                / f"{scene_number}.jpg"
            )

            print(
                f"Generating image "
                f"{scene_number}/"
                f"{len(prompt_batch.prompts)}..."
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

        # -----------------------------------------
        # 6. Final result
        # -----------------------------------------

        print(
            f"Generated "
            f"{len(generated_images)} "
            f"story images."
        )

        return generated_images