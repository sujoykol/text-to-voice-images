from google import genai

from app.core.config import settings


class StoryWriter:

    MODEL_NAME = "gemini-3.1-flash-lite"

    MIN_DURATION_MINUTES = 1.0
    MAX_DURATION_MINUTES = 30.0

    WORDS_PER_MINUTE = 130

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def generate_story(
        self,
        prompt: str,
        duration_minutes: float = 5.0,
    ) -> str:

        # -----------------------------------------
        # Validate input
        # -----------------------------------------

        if not prompt or not prompt.strip():
            raise ValueError(
                "story prompt is required"
            )

        if not (
            self.MIN_DURATION_MINUTES
            <= duration_minutes
            <= self.MAX_DURATION_MINUTES
        ):
            raise ValueError(
                "duration_minutes must be between "
                f"{self.MIN_DURATION_MINUTES} and "
                f"{self.MAX_DURATION_MINUTES}"
            )

        # -----------------------------------------
        # Calculate target word range
        # -----------------------------------------

        target_words = round(
            duration_minutes * self.WORDS_PER_MINUTE
        )

        minimum_words = round(
            target_words * 0.85
        )

        maximum_words = round(
            target_words * 1.15
        )

        # -----------------------------------------
        # Story generation instructions
        # -----------------------------------------

        system_prompt = """
You are a professional storyteller creating original stories
for high-quality narrated story-video content.

The story will be converted into AI narration.

Your job is to create a complete, emotionally engaging,
cinematic story based on the user's request.

==================================================
STORY STRUCTURE
==================================================

Create:

1. A strong opening that immediately creates curiosity.

2. Natural character development.

3. A meaningful conflict, challenge, mystery,
   decision, or emotional problem.

4. Gradually increasing tension or emotional investment.

5. A meaningful choice, realization, consequence,
   or transformation for the protagonist.

6. A clear resolution of the central conflict.

7. A memorable and emotionally resonant ending.

==================================================
ENDING
==================================================

The ending must:

- resolve the main conflict
- feel earned
- reflect the protagonist's journey
- connect naturally to the central theme
- leave an emotional impression
- avoid generic conclusions
- avoid introducing a new conflict
- avoid excessive moralizing
- preferably communicate meaning through
  the protagonist's final action or realization

The final paragraph should feel satisfying when
spoken aloud.

The final sentence should ideally leave the listener
with something meaningful to think about.

==================================================
EMOTIONAL STORYTELLING
==================================================

- Create emotional progression.
- Do not make every moment dramatic.
- Allow quiet moments between intense moments.
- Make important discoveries meaningful.
- Give decisions consequences.
- Avoid artificial emotional language.
- Make the audience care about the protagonist.

==================================================
NARRATION QUALITY
==================================================

The story will be converted to AI voice narration.

Therefore:

- use natural spoken language
- keep sentences clear when spoken aloud
- avoid unnecessarily complicated sentences
- use descriptive language where useful
- use dialogue only when meaningful
- avoid excessive dialogue
- create natural pauses
- avoid repetitive descriptions

==================================================
ORIGINALITY
==================================================

- Create an original story.
- Do not imitate a specific author.
- Do not copy known stories.
- Avoid unnecessary clichés.
- Stay faithful to the user's request.
- Do not introduce unrelated events.

==================================================
OUTPUT
==================================================

Return ONLY the finished story.

Do not include:

- title
- headings
- analysis
- explanations
- commentary
- word-count information
- notes about the writing process
"""

        # -----------------------------------------
        # Generate story
        # -----------------------------------------

        response = self.client.models.generate_content(
            model=self.MODEL_NAME,
            contents=f"""
{system_prompt}

==================================================
USER REQUEST
==================================================

{prompt.strip()}

==================================================
TARGET NARRATION LENGTH
==================================================

Target duration:

Approximately {duration_minutes:.1f} minutes.

Target word count:

Approximately {target_words} words.

Acceptable range:

{minimum_words}–{maximum_words} words.

Write naturally within this range.

Do not pad the story simply to reach the word count.
Do not sacrifice story quality for length.
""",
        )

        # -----------------------------------------
        # Validate Gemini response
        # -----------------------------------------

        if not response.text:
            raise ValueError(
                "Gemini returned an empty story"
            )

        story = response.text.strip()

        if not story:
            raise ValueError(
                "Gemini returned an empty story"
            )

        return story