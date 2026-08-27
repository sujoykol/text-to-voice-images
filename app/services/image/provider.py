from abc import ABC, abstractmethod
from pathlib import Path

from app.schemas.image_prompt import ImagePrompt


class ImageProvider(ABC):

    @abstractmethod
    def generate(
        self,
        image_prompt: ImagePrompt,
        output_path: Path,
        reference_images: list[Path] | None = None,
    ) -> Path:
        """
        Generate an image from an ImagePrompt.

        Optional reference images can be supplied to help
        preserve visual identity and continuity.
        """
        raise NotImplementedError
