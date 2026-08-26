from google import genai

from app.core.config import settings
from app.schemas.story_analysis import StoryAnalysis


class StoryAnalyzer:

    MODEL_NAME = "gemini-3.1-flash-lite"

    SYSTEM_PROMPT = """
You are a professional story analyst working inside
an AI storytelling production system.

Your job is to analyze the supplied story and convert it
into structured information that can be used by downstream
storytelling systems.

The analysis may later be used for:

- story understanding
- narration planning
- character consistency
- visual planning
- image generation
- scene generation
- story quality evaluation

==================================================
SOURCE OF TRUTH
==================================================

The supplied story is the ONLY source of truth.

Analyze the story itself.

Do not rewrite the story.

Do not add events.

Do not add characters.

Do not add locations.

Do not add objects.

Do not add backstory.

Do not add facts that are not supported by the story.

If information is unknown, do not invent it.

==================================================
FACTUAL CONSISTENCY
==================================================

Separate what the story explicitly establishes from
what could merely be inferred.

Never present an unsupported inference as a fact.

Do NOT invent:

- character age
- gender unless established
- skin tone
- hair color
- eye color
- facial features
- body type
- clothing
- accessories
- buildings
- architecture
- geography
- weather
- season
- historical period
- objects
- relationships
- occupations
- abilities
- dialogue
- motivations
- backstory
- events

unless the story explicitly provides them or they are
clearly established by the narrative.

A missing detail must remain unspecified.

==================================================
FACTS
==================================================

The facts field should contain important concrete facts
that are directly supported by the story.

Each fact should describe something that actually happens
or is explicitly established.

Do not place assumptions or creative additions into facts.

==================================================
CHARACTERS
==================================================

Extract only characters that actually exist in the story.

For every character:

- identify their name
- identify their role
- summarize their established description
- identify personality traits supported by their actions,
  decisions, dialogue, or narration

Do not invent physical appearance.

If appearance is not described, leave it unspecified.

==================================================
SETTING
==================================================

Describe the setting using only information established
by the story.

Do not add environmental details that are not supported.

==================================================
THEME
==================================================

Identify the central theme or themes that naturally emerge
from the story.

Do not force a moral.

If the story does not contain a clear moral, describe the
underlying emotional or thematic meaning instead.

==================================================
EMOTIONAL ARC
==================================================

Identify the major emotional stages of the story.

Base these on:

- events
- character decisions
- consequences
- internal realizations
- changes in relationships

Do not invent emotional states that are unsupported.

==================================================
KEY EVENTS
==================================================

Extract the major events in chronological order.

Only include events that actually occur in the story.

Do not create additional events.

==================================================
CLIMAX
==================================================

Identify the most important turning point, confrontation,
decision, discovery, or realization already present in
the story.

Do not invent a climax.

==================================================
RESOLUTION
==================================================

Explain how the central conflict is resolved.

The resolution must be based entirely on the story.

==================================================
CONCLUSION MEANING
==================================================

Explain the emotional or thematic meaning of the conclusion.

Do not force a moral.

Do not invent meaning that contradicts the story.

==================================================
SCENE EXTRACTION
==================================================

Scenes are intended for downstream image generation.

Each scene must represent a meaningful visual moment
already contained in the story.

If TARGET_SCENE_COUNT is provided:

- Aim for exactly TARGET_SCENE_COUNT scenes.
- Divide existing story material into visually distinct
  moments when necessary.
- Preserve chronological order.
- Never invent a new event to reach the requested count.
- Never introduce a new character.
- Never introduce a new location.
- Never introduce a new object.
- Never introduce unsupported actions.
- Never introduce unsupported environmental details.

A long event may be divided into multiple scenes when
each scene represents a different visual moment that
already exists in the story.

For example:

"Arun finds the box, opens it, and discovers a photograph."

can become:

1. Arun discovers the box.
2. Arun opens the box.
3. Arun sees the photograph.

These are separate visual moments already contained
in the story.

Do NOT split a single static moment into meaningless
duplicate scenes merely to increase the count.

If TARGET_SCENE_COUNT is not provided, determine the
natural number of scenes from the story.

==================================================
SCENE DESCRIPTION
==================================================

For every scene provide:

- scene number
- description
- location
- time
- mood
- characters
- visual elements

The description must explain what is visually happening.

==================================================
VISUAL ELEMENTS
==================================================

Visual elements must come from the story.

Only include:

- characters explicitly present
- objects explicitly mentioned
- locations explicitly established
- environmental details explicitly described
- actions that are visually observable

Do NOT add cinematic decoration.

==================================================
VISUAL ACCURACY
==================================================

FACTUAL ACCURACY > VISUAL RICHNESS

A simple accurate scene is better than a visually rich
scene containing invented information.

==================================================
OUTPUT
==================================================

Return ONLY structured data matching the StoryAnalysis schema.

Do not return:

- markdown
- explanations
- commentary
- reasoning
- additional fields
"""


    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )


    def analyze_story(
        self,
        story: str,
        target_scene_count: int | None = None,
    ) -> StoryAnalysis:

        # -----------------------------------------
        # Validate story
        # -----------------------------------------

        if not story or not story.strip():
            raise ValueError(
                "story cannot be empty"
            )

        # -----------------------------------------
        # Validate scene count
        # -----------------------------------------

        if target_scene_count is not None:

            if target_scene_count < 1:
                raise ValueError(
                    "target scene count must be greater than zero"
                )

        # -----------------------------------------
        # Build target instruction
        # -----------------------------------------

        if target_scene_count is None:

            target_instruction = (
                "Determine the natural number of "
                "meaningful scenes from the story."
            )

        else:

            target_instruction = (
                f"TARGET_SCENE_COUNT = "
                f"{target_scene_count}\n\n"
                f"Produce exactly "
                f"{target_scene_count} meaningful "
                f"visual scenes whenever the supplied "
                f"story contains enough distinct visual "
                f"moments. Divide existing events into "
                f"smaller visual moments when necessary. "
                f"Never invent story content merely to "
                f"reach the requested count."
            )

        # -----------------------------------------
        # Generate analysis
        # -----------------------------------------

        response = self.client.models.generate_content(
            model=self.MODEL_NAME,
            contents=f"""
{self.SYSTEM_PROMPT}

==================================================
TARGET SCENE INSTRUCTION
==================================================

{target_instruction}

==================================================
STORY
==================================================

{story.strip()}
""",
            config={
                "response_mime_type": "application/json",
                "response_schema": StoryAnalysis,
            },
        )

        # -----------------------------------------
        # Validate Gemini response
        # -----------------------------------------

        if not response.text:
            raise ValueError(
                "Gemini returned an empty story analysis"
            )

        analysis = StoryAnalysis.model_validate_json(
            response.text
        )

        # -----------------------------------------
        # Validate generated scenes
        # -----------------------------------------

        if not analysis.scenes:
            raise ValueError(
                "story analysis contains no scenes"
            )

        # -----------------------------------------
        # Validate requested scene count
        # -----------------------------------------

        if (
            target_scene_count is not None
            and len(analysis.scenes)
            != target_scene_count
        ):
            raise ValueError(
                f"Gemini generated "
                f"{len(analysis.scenes)} scenes, "
                f"but {target_scene_count} were requested"
            )

        # -----------------------------------------
        # Validate scene numbering
        # -----------------------------------------

        expected_numbers = list(
            range(1, len(analysis.scenes) + 1)
        )

        actual_numbers = [
            scene.scene_number
            for scene in analysis.scenes
        ]

        if actual_numbers != expected_numbers:
            raise ValueError(
                "scene numbers must be sequential "
                "starting from 1"
            )

        return analysis