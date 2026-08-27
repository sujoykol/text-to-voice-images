from app.schemas.image_prompt import ImagePrompt
from app.schemas.image_prompt_batch import ImagePromptBatch
from app.schemas.story_analysis import StoryAnalysis
from app.schemas.visual_bible import VisualBible
from app.services.scene_prompt_service import ScenePromptService


class BatchScenePromptService:

    def __init__(self) -> None:
        self.scene_prompt_service = ScenePromptService()

    def create_all_prompts(
        self,
        analysis: StoryAnalysis,
        visual_bible: VisualBible,
    ) -> ImagePromptBatch:

        if analysis is None:
            raise ValueError(
                "story analysis is required"
            )

        if visual_bible is None:
            raise ValueError(
                "visual bible is required"
            )

        if not analysis.scenes:
            raise ValueError(
                "story analysis contains no scenes"
            )

        scene_numbers = [
            scene.scene_number
            for scene in analysis.scenes
        ]

        if len(scene_numbers) != len(set(scene_numbers)):
            raise ValueError(
                "story analysis contains duplicate scene numbers"
            )

        prompts: list[ImagePrompt] = []

        for scene in analysis.scenes:

            print()
            print(
                f"Generating image prompt "
                f"for scene {scene.scene_number}..."
            )

            prompt = (
                self.scene_prompt_service
                .create_prompt(
                    analysis=analysis,
                    visual_bible=visual_bible,
                    scene_number=scene.scene_number,
                )
            )

            prompts.append(prompt)

        if len(prompts) != len(analysis.scenes):
            raise RuntimeError(
                "generated prompt count does not match "
                "scene count"
            )

        return ImagePromptBatch(
            prompts=prompts
        )