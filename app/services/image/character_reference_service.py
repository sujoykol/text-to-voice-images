from google import genai

from app.core.config import settings
from app.schemas.character_reference import CharacterReference
from app.schemas.visual_bible import CharacterVisual


class CharacterReferenceService:
    """
    Creates a persistent visual reference definition
    from one locked CharacterVisual.
    """

    MODEL_NAME = "gemini-3.1-flash-lite"

    SYSTEM_PROMPT = """
You are a professional character visual-development
director working inside an AI storytelling production
system.

Your task is to create ONE production-ready character
reference definition from ONE locked CharacterVisual.

The resulting reference will be used as a persistent
visual identity for image generation across many scenes.

==================================================
PRIMARY GOAL
==================================================

Create a stable visual identity for the character.

The character reference must make the character
recognizable and visually consistent across future
images.

==================================================
LOCKED DATA
==================================================

The supplied CharacterVisual is the source of truth.

You MUST preserve every supplied attribute exactly.

You MUST NOT:

- change the character's identity
- change the age
- change the gender
- change physical appearance
- change clothing
- remove distinctive features
- contradict consistency notes

==================================================
CREATIVE DECISIONS
==================================================

Creative decisions are allowed ONLY when the supplied
CharacterVisual does not define enough information for
a useful visual reference.

Creative decisions may establish:

- neutral pose
- neutral expression
- simple presentation
- clean visual composition
- suitable reference framing

Do NOT create:

- new backstory
- new personality
- new plot information
- new accessories
- new clothing
- new distinctive features

==================================================
REFERENCE IMAGE PURPOSE
==================================================

This is NOT a story scene.

Do NOT place the character:

- in a village
- in a house
- in a forest
- at a workplace
- during a story event

unless such information is explicitly part of the
character's permanent visual identity.

The reference should focus on the character itself.

==================================================
REFERENCE PRESENTATION
==================================================

The reference prompt should request:

- full character visibility
- clear face
- clear hairstyle when established
- clear clothing
- stable body proportions
- neutral standing pose
- unobstructed character
- clean readable presentation
- simple background
- consistent 2D illustration style

Avoid dramatic cinematic composition.

The purpose is character identity, not storytelling.

==================================================
VISUAL STYLE
==================================================

Use the supplied visual style when available.

The character reference should visually belong to
the same overall illustration language as the story.

==================================================
PROMPT QUALITY
==================================================

The generated reference prompt must:

1. Name the character.
2. Explicitly preserve every non-null locked attribute.
3. Request a full-body view from head to toe.
4. Request a neutral standing pose.
5. Request a clear unobstructed face.
6. Request stable body proportions.
7. Preserve the supplied visual style.
8. Avoid adding unsupported physical characteristics.
9. Avoid turning the reference into a story scene.

==================================================
OUTPUT
==================================================

Return ONLY structured data matching the
CharacterReference schema.

Do not return markdown.
Do not return explanations.
Do not return reasoning.
"""

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def create_reference(
        self,
        character: CharacterVisual,
        visual_style: str | None = None,
    ) -> CharacterReference:
        """
        Create one persistent character reference definition.
        """

        if character is None:
            raise ValueError(
                "character is required"
            )

        locked_character_data = {
            "name": character.name,
            "story_description": (
                character.story_description
            ),
            "age": (
                character.age.value
                if character.age
                else None
            ),
            "gender": (
                character.gender.value
                if character.gender
                else None
            ),
            "physical_appearance": (
                character.physical_appearance.value
                if character.physical_appearance
                else None
            ),
            "clothing": (
                character.clothing.value
                if character.clothing
                else None
            ),
            "distinctive_features": [
                feature.value
                for feature in character.distinctive_features
            ],
            "consistency_notes": (
                character.consistency_notes
            ),
        }

        response = self.client.models.generate_content(
            model=self.MODEL_NAME,
            contents=f"""
{self.SYSTEM_PROMPT}

==================================================
LOCKED CHARACTER DATA
==================================================

The following character information is immutable.

{locked_character_data}

==================================================
VISUAL STYLE
==================================================

{visual_style or "Cinematic 2D digital illustration."}

==================================================
FINAL REQUIREMENTS
==================================================

Create the persistent character reference for:

{character.name}

Every non-null locked attribute MUST be represented
faithfully in the reference prompt.

The reference must show the complete character
from head to toe.

Use a neutral standing pose.

Use a simple unobstructed presentation.

Do not place the character inside a story scene.

Do not invent unsupported physical characteristics.

Return ONLY CharacterReference structured data.
""",
            config={
                "response_mime_type": "application/json",
                "response_schema": CharacterReference,
            },
        )

        if not response.text:
            raise ValueError(
                "Gemini returned an empty character reference"
            )

        return CharacterReference.model_validate_json(
            response.text
        )

