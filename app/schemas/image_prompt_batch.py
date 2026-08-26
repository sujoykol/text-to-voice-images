from pydantic import BaseModel

from app.schemas.image_prompt import ImagePrompt


class ImagePromptBatch(BaseModel):
    prompts: list[ImagePrompt]
