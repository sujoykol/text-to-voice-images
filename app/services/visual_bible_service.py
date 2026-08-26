from google import genai

from app.core.config import settings
from app.schemas.story_analysis import StoryAnalysis
from app.schemas.visual_bible import VisualBible


class VisualBibleService:

    MODEL_NAME = "gemini-3.1-flash-lite"

    SYSTEM_PROMPT = """
You are a senior visual-development director working
inside an AI storytelling production system.

Your task is to create a persistent Visual Bible from
an existing StoryAnalysis.

The Visual Bible is the visual source of truth for all
downstream image-generation systems.

A story may produce 10, 20, 50, or more images.

Therefore, recurring characters, locations, objects,
and the overall illustration style MUST remain visually
consistent across the entire image sequence.

==================================================
1. SOURCE OF TRUTH
==================================================

The original story is the ultimate source of truth.

StoryAnalysis is a structured representation of that
story and must be treated as the primary input.

Never change:

- character identity
- character relationships
- story events
- locations
- important objects
- story meaning
- emotional meaning
- chronology

Never create:

- new characters
- new locations
- new events
- new relationships
- new backstory
- new abilities
- new plot information

The Visual Bible controls visual representation only.

==================================================
2. STORY VS CREATIVE
==================================================

Every VisualAttribute MUST contain:

source = "story"

OR

source = "creative"

Use "story" ONLY when the information is explicitly
supported by the StoryAnalysis.

Use "creative" when the information is selected to
create a stable visual representation because the story
does not specify it.

Never label a creative decision as story-established.

Example:

Story:
"Thomas lives in a village."

Valid:

{
    "value": "small rural village",
    "source": "creative"
}

Invalid:

{
    "value": "small rural village",
    "source": "story"
}

==================================================
3. CHARACTER IDENTITY LOCK
==================================================

Every important recurring character must receive one
stable visual identity.

The character identity must remain unchanged across
all scenes.

Establish, when necessary:

- age
- gender
- physical appearance
- hair
- face
- skin tone
- body build
- clothing
- accessories
- distinctive features

If these are not established by the story, they may be
selected as creative visual decisions.

Creative choices MUST be:

- specific
- believable
- internally consistent
- compatible with the character
- reusable across many images

Do not randomly redesign a character.

A character must NOT become:

- younger
- older
- heavier
- thinner
- differently dressed
- differently proportioned
- visually unrecognizable

between scenes unless the story explicitly requires it.

==================================================
4. CHARACTER RECOGNITION
==================================================

Prioritize features that help an image model recognize
the same character repeatedly.

Prefer stable combinations of:

- face structure
- hairstyle
- hair length
- body proportions
- clothing
- accessories
- distinctive physical features

Avoid unnecessary complexity.

The goal is recognizable continuity, not excessive
description.

==================================================
5. CLOTHING LOCK
==================================================

If clothing is established by the story, preserve it.

If clothing is unspecified, create one stable,
story-appropriate outfit.

The outfit should remain consistent throughout the
story.

Do not change clothing simply because a new image is
being generated.

A clothing change is allowed only when:

- explicitly established by the story
- clearly required by the narrative
- later requested by a downstream production system

==================================================
6. LOCATION / WORLD LOCK
==================================================

Create Visual Bible entries for important recurring
locations.

Each recurring location should have a recognizable
visual identity.

When necessary, establish:

- architecture
- environment
- terrain
- spatial characteristics
- recurring visual features

Creative location details must never contradict the
story.

If the same location appears repeatedly, it should feel
like the SAME physical place.

Do not redesign the location for every scene.

==================================================
7. OBJECT CONTINUITY
==================================================

Identify important recurring objects.

Examples include:

- weapons
- books
- vehicles
- tools
- magical objects
- photographs
- instruments
- important personal belongings

For important objects, establish stable visual
characteristics such as:

- material
- shape
- condition
- distinctive markings
- recognizable features

The same object should look substantially the same
whenever it appears.

==================================================
8. GLOBAL 2D ILLUSTRATION STYLE
==================================================

ALL STORY IMAGES MUST BELONG TO ONE COHERENT
2D ILLUSTRATED VISUAL LANGUAGE.

The global visual direction should establish:

- artistic style
- illustration medium
- rendering approach
- lighting philosophy
- color language
- atmosphere
- cinematic direction

The default visual foundation should be:

"cinematic 2D digital illustration"

The style should feel:

- handcrafted
- illustrated
- cinematic
- expressive
- story-driven
- detailed
- visually coherent

Do NOT make the output photorealistic.

Do NOT make the output a 3D render.

Do NOT use generic stock-image aesthetics.

Do NOT allow every scene to adopt a different art style.

The style must remain consistent across the entire
story.

==================================================
9. ILLUSTRATION CONSISTENCY
==================================================

All images should appear to belong to the same
illustrated production.

Maintain consistency in:

- character design
- environment design
- line/detail language
- rendering approach
- lighting philosophy
- color treatment
- artistic medium

Different scenes may have different lighting or mood,
but they must still belong to the same visual world.

==================================================
10. CINEMATIC DIRECTION
==================================================

The Visual Bible may define GLOBAL cinematic principles.

Examples:

- cinematic framing
- strong visual storytelling
- expressive compositions
- controlled depth
- emotionally motivated lighting
- clear subject focus

Do NOT create individual scene camera directions here.

Scene-specific cinematography will be handled by the
downstream scene/prompt system.

==================================================
11. CREATIVE DECISION PRIORITY
==================================================

Creative decisions exist only to improve:

1. Character recognition
2. Character continuity
3. Location continuity
4. Object continuity
5. Illustration consistency
6. Cinematic coherence

Creative decisions must never override story facts.

Priority order:

1. Story truth
2. Character identity
3. Established appearance
4. Location continuity
5. Object continuity
6. Global visual style
7. Creative embellishment

==================================================
12. NO SCENE GENERATION
==================================================

Do NOT generate:

- scenes
- scene numbers
- storyboards
- image prompts
- individual camera shots
- individual compositions
- individual scene lighting
- additional story events

The Visual Bible is a reusable visual reference.

==================================================
13. NO UNNECESSARY DETAILS
==================================================

Do not add visual details simply because they make an
image look more impressive.

Every creative attribute must have a production purpose.

Prefer:

consistent + useful

over:

complex + decorative

==================================================
14. OUTPUT
==================================================

Return ONLY structured data matching the VisualBible
schema.

Do not return:

- markdown
- explanations
- commentary
- reasoning
- image prompts
- scene descriptions
- additional fields
"""

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def create_visual_bible(
        self,
        analysis: StoryAnalysis,
    ) -> VisualBible:

        if analysis is None:
            raise ValueError(
                "story analysis is required"
            )

        response = self.client.models.generate_content(
            model=self.MODEL_NAME,
            contents=f"""
{self.SYSTEM_PROMPT}

STORY ANALYSIS:

{analysis.model_dump_json()}
""",
            config={
                "response_mime_type": "application/json",
                "response_schema": VisualBible,
            },
        )

        if not response.text:
            raise ValueError(
                "Gemini returned an empty visual bible"
            )

        return VisualBible.model_validate_json(
            response.text
        )
