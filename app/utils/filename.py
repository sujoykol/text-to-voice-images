import re
import unicodedata
from pathlib import Path


def safe_filename(
    text: str,
    extension: str = ".mp3",
    max_length: int = 80,
) -> str:
    """
    Convert human-readable text into a safe filesystem filename.

    Example:
        "The Treasure Beneath the Soil"
        -> "the_treasure_beneath_the_soil.mp3"
    """

    text = unicodedata.normalize("NFKD", text)

    text = text.encode(
        "ascii",
        "ignore",
    ).decode("ascii")

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9]+",
        "_",
        text,
    )

    text = text.strip("_")

    text = text[:max_length].rstrip("_")

    if not text:
        text = "story"

    extension = extension if extension.startswith(".") else f".{extension}"

    return f"{text}{extension}"
def safe_folder_name(
    text: str,
    max_length: int = 50,
) -> str:
    """
    Convert human-readable text into a safe,
    short filesystem folder name.

    Example:
        "The Treasure Beneath the Soil"
        -> "the_treasure_beneath_the_soil"
    """

    text = unicodedata.normalize(
        "NFKD",
        text,
    )

    text = text.encode(
        "ascii",
        "ignore",
    ).decode("ascii")

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9]+",
        "_",
        text,
    )

    text = text.strip("_")

    text = text[:max_length].rstrip("_")

    if not text:
        text = "story"

    return text
