from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Schemas for My Adventure Tale ---
class StoryStartRequest(BaseModel):
    theme: str

class StoryChoiceRequest(BaseModel):
    story_history: List[Dict[str, Any]] # Using Any for parts content type
    choice_text: str

class StorySegmentResponse(BaseModel):
    story_text: str
    image_prompt: str
    choices: List[str]
    updated_story_history: List[Dict[str, Any]] # Using Any for parts content type


# --- Old Schemas (from Item CRUD example, can be removed if Item API is fully removed) ---
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    """Schema for creating a new item"""
    pass

class ItemUpdate(BaseModel):
    """Schema for updating an existing item"""
    name: Optional[str] = None
    description: Optional[str] = None

class ItemResponse(ItemBase):
    """Schema for returning item data in responses"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True # Updated from orm_mode for Pydantic V2 compatibility 