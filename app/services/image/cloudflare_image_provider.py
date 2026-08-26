import base64
from pathlib import Path

import requests

from app.core.config import settings
from app.schemas.image_prompt import ImagePrompt
from app.services.image.provider import ImageProvider


class CloudflareImageProvider(ImageProvider):

    MODEL_NAME = "@cf/black-forest-labs/flux-1-schnell"

    def generate(
        self,
        image_prompt: ImagePrompt,
        output_path: Path,
    ) -> Path:

        if image_prompt is None:
            raise ValueError(
                "image prompt is required"
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{settings.CLOUDFLARE_ACCOUNT_ID}/ai/run/"
            f"{self.MODEL_NAME}"
        )

        headers = {
            "Authorization": (
                f"Bearer {settings.CLOUDFLARE_API_TOKEN}"
            ),
            "Content-Type": "application/json",
        }

        payload = {
            "prompt": image_prompt.prompt,
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=120,
            )

            response.raise_for_status()

            data = response.json()

            image_base64 = data["result"]["image"]

            image_bytes = base64.b64decode(
                image_base64
            )

            output_path.write_bytes(
                image_bytes
            )

            return output_path

        except Exception as exc:
            raise RuntimeError(
                f"Cloudflare image generation failed: {exc}"
            ) from exc