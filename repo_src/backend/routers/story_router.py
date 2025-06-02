from fastapi import APIRouter, HTTPException
from typing import List 

from repo_src.backend.data.schemas import (
    StoryStartRequest,
    StoryChoiceRequest,
    StorySegmentResponse
)
from repo_src.backend.llm_services.story_generator import generate_story_segment

router = APIRouter(
    prefix="/api/story",
    tags=["story"],
)

@router.post("/start", response_model=StorySegmentResponse)
async def start_new_story(request: StoryStartRequest):
    try:
        story_text, image_prompt, choices, updated_history = await generate_story_segment(
            theme=request.theme
        )
        return StorySegmentResponse(
            story_text=story_text,
            image_prompt=image_prompt,
            choices=choices,
            updated_story_history=updated_history
        )
    except Exception as e:
        print(f"Error in /start endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to start story.")

@router.post("/continue", response_model=StorySegmentResponse)
async def continue_story(request: StoryChoiceRequest):
    if not request.story_history or not request.choice_text:
        raise HTTPException(status_code=400, detail="Story history and choice text are required.")
    try:
        story_text, image_prompt, choices, updated_history = await generate_story_segment(
            story_history=request.story_history,
            user_choice=request.choice_text
        )
        return StorySegmentResponse(
            story_text=story_text,
            image_prompt=image_prompt,
            choices=choices,
            updated_story_history=updated_history
        )
    except Exception as e:
        print(f"Error in /continue endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to continue story.") 