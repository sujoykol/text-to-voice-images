from pydantic import BaseModel


class GeneratedImage(BaseModel):
    scene_number: int
    filename: str


class ImageGenerationResponse(BaseModel):
    message: str
    images: list[GeneratedImage]
