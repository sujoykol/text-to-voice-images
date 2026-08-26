from app.services.story_writer import StoryWriter


writer = StoryWriter()

story = writer.generate_story(
    """
    Write a short emotional moral story about a poor farmer
    who discovers an unexpected treasure.
    """
)

print("\n===== GENERATED STORY =====\n")
print(story)
