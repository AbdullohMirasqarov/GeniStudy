from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class VideoCreate(BaseModel):
    title: str
    order: Optional[int] = 1

class VideoOut(BaseModel):
    id: UUID
    title: str  
    order: int
    video_url: Optional[str] = None  # Video URL may not be available at creation

    model_config = {
        "from_attributes": True
    }