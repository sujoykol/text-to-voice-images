from app.services.narration_director import NarrationDirector


story = """
In a small village in India, a clever shopkeeper named Govind
ran a modest shop. A humble farmer named Ramu visited his shop
every morning. One day, Govind became suspicious that Ramu was
cheating him. He weighed Ramu's butter and discovered that it
weighed only 900 grams.
"""


director = NarrationDirector()

plan = director.create_narration_plan(story)

print(plan.model_dump_json(indent=2))
