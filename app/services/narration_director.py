from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.narration import NarrationPlan


class NarrationDirector:
    """
    Converts a story into a structured performance plan
    for an AI storyteller voice.
    """

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def create_narration_plan(self, story: str) -> NarrationPlan:
        prompt = f"""
You are an expert cinematic narrator and professional voice director.

Your task is to transform the supplied story into a natural,
emotionally engaging narration performance plan for an AI voice actor.

The final narration should sound like a professional human storyteller,
not like a text-to-speech system simply reading sentences.

==================================================
STORY SEGMENTATION
==================================================

Divide the story into natural spoken segments.

A segment should normally contain one meaningful thought, action,
event, or emotional beat.

Do not split the story mechanically sentence-by-sentence when
two sentences naturally belong together.

Do not create unnecessarily short segments.

Do not combine unrelated events into one segment.

Preserve the chronological order of the story.

==================================================
SEGMENT FIELDS
==================================================

For every segment determine:

1. The narration text.
2. The primary emotion.
3. Emotional intensity from 0.0 to 1.0.
4. Speaking pace.
5. Pause after the segment.
6. Important words that deserve vocal emphasis.

==================================================
AVAILABLE EMOTIONS
==================================================

peaceful
happy
sad
angry
fearful
suspense
surprise
hopeful
dramatic
reflective
neutral

==================================================
AVAILABLE PACES
==================================================

very_slow
slow
normal
fast
very_fast

==================================================
EMOTIONAL DIRECTION
==================================================

Use "neutral" for ordinary factual narration.

Use "peaceful" for calm, warm, pleasant, or welcoming moments.

Use "happy" for genuine joy or positive events.

Use "sad" for genuine sadness, loss, disappointment, or grief.

Use "angry" when strong anger is actually present.

Use "fearful" when the situation creates fear or danger.

Use "suspense" when the listener should anticipate what will happen next.

Use "surprise" for an unexpected discovery, revelation, or sudden change.

Use "dramatic" only for genuinely important dramatic moments.

Use "hopeful" for optimism, positive resolution, or encouragement.

Use "reflective" for wisdom, realization, moral lessons, or thoughtful conclusions.

Do not make every segment emotional.

Emotional intensity must match the actual importance of the moment.

==================================================
INTENSITY
==================================================

0.0 - 0.2  = almost neutral
0.3 - 0.4  = subtle emotion
0.5 - 0.6  = noticeable emotion
0.7 - 0.8  = strong emotion
0.9 - 1.0  = extremely strong emotion

Do not use high intensity simply to make narration sound dramatic.

Reserve 0.8+ for important emotional moments.

==================================================
PACING
==================================================

Use:

very_slow:
major revelation, deep reflection, emotional ending

slow:
suspense, important information, emotional moments

normal:
ordinary narration and normal storytelling

fast:
urgency, excitement, rapid action

very_fast:
rarely use; only when the story genuinely requires extreme urgency

Important revelations should generally be slower than ordinary narration.

==================================================
PAUSES
==================================================

Pause after the segment using seconds.

Normal narration:
0.2 - 0.6 seconds

Scene transition:
0.6 - 1.0 seconds

Suspense:
0.7 - 1.5 seconds

Major revelation:
1.0 - 2.0 seconds

Moral or final conclusion:
1.0 - 2.0 seconds

Avoid 0.0 unless absolutely necessary.

Do not make every pause long.

The rhythm should feel natural to a human listener.

==================================================
EMPHASIS
==================================================

Use emphasis sparingly.

Only include words or short phrases that genuinely deserve
extra vocal attention.

Good examples:

- character names when introduced
- important numbers
- discoveries
- critical objects
- important revelations
- key moral concepts

Do NOT emphasize ordinary words just because they appear
important in the sentence.

Prefer short phrases rather than entire sentences.

==================================================
STORYTELLING RULES
==================================================

1. Preserve the meaning of the original story.

2. Do not invent events.

3. Do not invent dialogue.

4. Do not invent character emotions that are unsupported
   by the story.

5. Do not change factual details.

6. Keep the narration natural when spoken aloud.

7. Avoid repetitive emotional changes.

8. Use emotional transitions gradually when appropriate.

9. Important moments should receive more vocal space than
   ordinary information.

10. The beginning should normally establish the setting and
    characters naturally.

11. Build suspense gradually rather than immediately using
    maximum intensity.

12. Major revelations should feel significant.

13. The ending or moral should normally feel slower and
    more reflective.

==================================================
QUALITY TARGET
==================================================

Imagine this narration will be used for a professional
YouTube storytelling channel.

The listener should feel that a skilled human narrator is
telling the story with controlled emotion, natural pacing,
and deliberate pauses.

Avoid theatrical overacting.

Subtle emotion is often better than excessive emotion.

==================================================
STORY
==================================================

{story}
"""

        response = self.client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=NarrationPlan,
            ),
        )

        return NarrationPlan.model_validate_json(response.text)