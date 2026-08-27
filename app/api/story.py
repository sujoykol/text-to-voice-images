from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.schemas.story import (
    StoryGenerateRequest,
    StoryGenerateResponse,
)
from app.schemas.story_analysis import (
    StoryAnalysis,
    StoryAnalysisRequest,
    StoryImageGenerationRequest,
)
from app.services.story_audio_service import StoryAudioService
from app.services.story_analyzer import StoryAnalyzer
from app.services.visual_bible_service import VisualBibleService
from app.schemas.visual_bible import VisualBible

from app.schemas.image_generation import (
    GeneratedImage,
    ImageGenerationResponse,
)
from app.services.story_image_service import StoryImageService

router = APIRouter(
    prefix="/api/v1/story",
    tags=["Story"],
)


story_audio_service = StoryAudioService()
story_analyzer = StoryAnalyzer()
visual_bible_service = VisualBibleService()
story_image_service = StoryImageService()


@router.post(
    "/generate",
    response_model=StoryGenerateResponse,
)
def generate_story_audio(
    request: StoryGenerateRequest,
) -> StoryGenerateResponse:

    try:

        output_path = story_audio_service.generate_story_audio(
            mode=request.mode,
            prompt=request.prompt,
            story=request.story,
            duration_minutes=request.duration_minutes,
            language=request.language,
            voice=request.voice,
            speed=request.speed,
        )

        return StoryGenerateResponse(
            message="Story MP3 generated successfully",
            filename=output_path.name,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        print(
            f"Story audio generation error: "
            f"{type(exc).__name__}: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.post(
    "/analyze",
    response_model=StoryAnalysis,
)
def analyze_story(
    request: StoryAnalysisRequest,
) -> StoryAnalysis:

    try:
        return story_analyzer.analyze_story(
            request.story
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to analyze story",
        ) from exc


@router.get(
    "/audio/{filename}",
)
def get_story_audio(
    filename: str,
) -> FileResponse:

    audio_dir = Path("audio")
    file_path = audio_dir / filename

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Audio file not found",
        )

    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=file_path.name,
    )

@router.post(
    "/images",
)
def generate_story_images(
    request: StoryImageGenerationRequest,
):

    try:
        generated_images = (
            story_image_service
            .generate_story_images(
                story=request.story,
                image_count=request.image_count,
            )
        )

        return {
            "message": (
                "Story images generated successfully"
            ),
            "image_count": len(
                generated_images
            ),
            "images": [
                str(path)
                for path in generated_images
            ],
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        print(
            f"Story image generation error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to generate story images",
        ) from exc    

@router.post(
    "/visual-bible",
    response_model=VisualBible,
)
def create_visual_bible(
    request: StoryAnalysisRequest,
) -> VisualBible:

    try:
        analysis = story_analyzer.analyze_story(
            request.story
        )

        return visual_bible_service.create_visual_bible(
            analysis
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to create visual bible",
        ) from exc    

@router.get(
    "/images/{story_name}/{filename}",
)
def get_story_image(
    story_name: str,
    filename: str,
) -> FileResponse:

    images_root = Path("images").resolve()

    story_dir = (
        images_root / story_name
    ).resolve()

    image_path = (
        story_dir / filename
    ).resolve()

    # Prevent path traversal
    if images_root not in image_path.parents:
        raise HTTPException(
            status_code=400,
            detail="Invalid image path",
        )

    if not image_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Image not found",
        )

    return FileResponse(
        path=image_path,
        media_type="image/jpeg",
        filename=image_path.name,
    )        