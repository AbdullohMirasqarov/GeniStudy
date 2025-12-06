from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.course import CourseCategory, CourseSubCategory
from app.schemas.category import CategoryBase, SubCategoryBase
from app.schemas.category import CategoryOut, SubCategoryOut
from fastapi import status
from typing import List
from uuid import UUID
from app.dependencies import teacher_only


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


def _pydantic_to_dict(data):
    """
    Pydantic v1 va v2 bilan ishlash uchun util.
    Agar model_dump mavjud bo'lsa (v2) — shu, aks holda .dict() (v1).
    """
    if hasattr(data, "model_dump"):
        return data.model_dump()
    if hasattr(data, "dict"):
        return data.dict()
    # Fallback: agar oddiy dict kelsa
    return dict(data)



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryBase, 
    db: Session = Depends(get_db),
    current_user=Depends(teacher_only)
):
    payload = _pydantic_to_dict(data)

    existing = db.query(CourseCategory).filter(CourseCategory.name == payload["name"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bunday nomli category allaqachon mavjud.")

    category = CourseCategory(
        name=payload.get("name"),
        description=payload.get("description", "") or ""
    )
    db.add(category)
    db.commit()
    db.refresh(category)

    return {
        "id": category.id,
        "name": category.name,
        "description": category.description
    }



@router.get("/", response_model=List[dict])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(CourseCategory).order_by(CourseCategory.name).all()
    result = []
    for c in categories:
        result.append({
            "id": c.id,
            "name": c.name,
            "description": c.description
        })
    return result


@router.get("/{category_id}")
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    category = db.query(CourseCategory).filter(CourseCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category topilmadi.")

    # Subcategories ro'yxati (agar mavjud bo'lsa)
    subs = []
    for s in getattr(category, "subcategories", []):
        subs.append({
            "id": s.id,
            "name": s.name
        })

    return {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "subcategories": subs
    }

@router.post("/subcategory")
def create_subcategory(
    data: SubCategoryBase, 
    db: Session = Depends(get_db),
    current_user=Depends(teacher_only)
):
    category = db.query(CourseCategory).filter(CourseCategory.id == data.category_id).first()
    if not category:
        raise HTTPException(404, "Category topilmadi")

    sub = CourseSubCategory(**data.model_dump())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub