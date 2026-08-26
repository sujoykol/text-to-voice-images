from abc import ABC, abstractmethod
from pathlib import Path

from app.schemas.image_prompt import ImagePrompt


class ImageProvider(ABC):

    @abstractmethod
    def generate(
        self,
        image_prompt: ImagePrompt,
        output_path: Path,
    ) -> Path:
        """
        Generate an image from an ImagePrompt
        and save it to output_path.
        """
        raise NotImplementedError
