from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = ""

class CategoryOut(CategoryBase):
    id: UUID

    model_config = {
        "from_attributes": True
    }


class SubCategoryBase(BaseModel):
    name: str
    category_id: UUID


class SubCategoryOut(SubCategoryBase):
    id: UUID

    model_config = {
        "from_attributes": True
    }
