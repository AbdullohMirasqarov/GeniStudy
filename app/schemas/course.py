from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from .video import VideoOut
from typing import List

class CourseCreate(BaseModel):
    name: str
    description: Optional[str]
    image_url: Optional[str]
    price: int
    category_id: UUID
    subcategory_id: Optional[UUID]


class CourseUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    price: Optional[int]

class CourseOut(BaseModel):
    id: UUID
    name: str
    description: str
    price: int
    image_url: Optional[str]
    videos: List[VideoOut] = []

    model_config = {
        "from_attributes": True
    }


class CourseOutWithoutVideos(BaseModel):
    id: UUID
    name: str
    description: str
    price: int
    image_url: Optional[str]

    model_config = {
        "from_attributes": True
    }

class CoursePreview(BaseModel):
    id: UUID
    name: str
    image_url: str
    is_purchased: bool = False

    model_config = {
        "from_attributes": True
    }