from app.services.story_audio_service import StoryAudioService


story = """
In a small village in India, a clever shopkeeper named Govind
ran a modest shop that had been in his family for three generations.

Although the villagers trusted him, Govind was secretly greedy
and deceitful.

Every morning, a humble farmer named Ramu rode his bicycle
three kilometers to Govind's shop.

Ramu's wife Kamla made the finest butter in the village.

For five years, they had a simple agreement.

Ramu gave Govind one kilogram of fresh butter,
and Govind gave Ramu one kilogram of wheat.

One hot summer morning, Govind became suspicious.

He wondered whether Ramu had been cheating him.

So Govind weighed the butter himself.

To his shock, the butter weighed only nine hundred grams.

But the truth was very different.

Ramu did not own a proper weighing scale.

Every day, he used the one kilogram of wheat
he received from Govind to measure the butter.

The villagers suddenly understood what had happened.

Govind had been giving Ramu only nine hundred grams of wheat.

His own dishonesty had come back to him.

The Panchayat ordered Govind to repay what he owed
and he was banished from the village.

The villagers learned an important lesson:

What we do to others often comes back to us.
"""


service = StoryAudioService()

output = service.generate_story_audio(
    story,
    output_name="govind_story.wav",
)

print(f"Done: {output}")
