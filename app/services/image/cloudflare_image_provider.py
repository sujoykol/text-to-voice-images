import base64
import mimetypes
from pathlib import Path

import requests

from app.core.config import settings
from app.schemas.image_prompt import ImagePrompt
from app.services.image.provider import ImageProvider


class CloudflareImageProvider(ImageProvider):

    MODEL_NAME = "@cf/black-forest-labs/flux-2-klein-4b"

    # Image generation can take longer than a normal API request.
    CONNECT_TIMEOUT = 30
    READ_TIMEOUT = 300

    MAX_REFERENCE_IMAGES = 4

    def generate(
        self,
        image_prompt: ImagePrompt,
        output_path: Path,
        reference_images: list[Path] | None = None,
    ) -> Path:

        # --------------------------------------------------
        # Validate prompt
        # --------------------------------------------------

        if image_prompt is None:
            raise ValueError(
                "image prompt is required"
            )

        if not image_prompt.prompt.strip():
            raise ValueError(
                "image prompt cannot be empty"
            )

        # --------------------------------------------------
        # Validate reference images
        # --------------------------------------------------

        if reference_images is None:
            reference_images = []

        if len(reference_images) > self.MAX_REFERENCE_IMAGES:
            raise ValueError(
                f"maximum {self.MAX_REFERENCE_IMAGES} "
                "reference images are supported"
            )

        for image_path in reference_images:

            if not image_path.exists():
                raise FileNotFoundError(
                    f"reference image not found: "
                    f"{image_path}"
                )

            if not image_path.is_file():
                raise ValueError(
                    f"reference image is not a file: "
                    f"{image_path}"
                )

        # --------------------------------------------------
        # Prepare output directory
        # --------------------------------------------------

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # --------------------------------------------------
        # Cloudflare endpoint
        # --------------------------------------------------

        url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{settings.CLOUDFLARE_ACCOUNT_ID}/ai/run/"
            f"{self.MODEL_NAME}"
        )

        headers = {
            "Authorization": (
                f"Bearer {settings.CLOUDFLARE_API_TOKEN}"
            ),
        }

        # --------------------------------------------------
        # Multipart request
        # --------------------------------------------------

        files = {
            "prompt": (
                None,
                image_prompt.prompt,
            ),
            "width": (
                None,
                "1024",
            ),
            "height": (
                None,
                "1024",
            ),
        }

        opened_files = []

        try:

            # ----------------------------------------------
            # Attach reference images
            # ----------------------------------------------

            for index, image_path in enumerate(
                reference_images
            ):

                file_handle = open(
                    image_path,
                    "rb",
                )

                opened_files.append(
                    file_handle
                )

                mime_type, _ = mimetypes.guess_type(
                    image_path.name
                )

                if mime_type is None:
                    mime_type = "application/octet-stream"

                files[
                    f"input_image_{index}"
                ] = (
                    image_path.name,
                    file_handle,
                    mime_type,
                )

            # ----------------------------------------------
            # Generate image
            # ----------------------------------------------

            print(
                "Sending image generation request "
                "to Cloudflare..."
            )

            response = requests.post(
                url,
                headers=headers,
                files=files,
                timeout=(
                    self.CONNECT_TIMEOUT,
                    self.READ_TIMEOUT,
                ),
            )

            # ----------------------------------------------
            # HTTP validation
            # ----------------------------------------------

            if not response.ok:
                raise RuntimeError(
                    f"Cloudflare API error "
                    f"{response.status_code}: "
                    f"{response.text}"
                )

            # ----------------------------------------------
            # Parse response
            # ----------------------------------------------

            data = response.json()

            if not data.get("success"):
                raise RuntimeError(
                    "Cloudflare API returned failure: "
                    f"{data}"
                )

            result = data.get("result")

            if not result:
                raise RuntimeError(
                    "Cloudflare API returned an empty result"
                )

            image_base64 = result.get("image")

            if not image_base64:
                raise RuntimeError(
                    "Cloudflare API response does not "
                    "contain an image"
                )

            # ----------------------------------------------
            # Decode image
            # ----------------------------------------------

            try:
                image_bytes = base64.b64decode(
                    image_base64
                )
            except Exception as exc:
                raise RuntimeError(
                    "Cloudflare returned invalid "
                    "base64 image data"
                ) from exc

            if not image_bytes:
                raise RuntimeError(
                    "Cloudflare returned empty image data"
                )

            # ----------------------------------------------
            # Save image
            # ----------------------------------------------

            output_path.write_bytes(
                image_bytes
            )

            print(
                f"Image generated: {output_path}"
            )

            return output_path

        except requests.exceptions.ConnectTimeout as exc:

            raise RuntimeError(
                "Cloudflare connection timed out. "
                "Please check network connectivity."
            ) from exc

        except requests.exceptions.ReadTimeout as exc:

            raise RuntimeError(
                "Cloudflare image generation timed out "
                f"after {self.READ_TIMEOUT} seconds."
            ) from exc

        except requests.exceptions.RequestException as exc:

            raise RuntimeError(
                "Cloudflare request failed: "
                f"{exc}"
            ) from exc

        except Exception as exc:

            raise RuntimeError(
                "Cloudflare image generation failed: "
                f"{exc}"
            ) from exc

        finally:

            for file_handle in opened_files:
                file_handle.close()
