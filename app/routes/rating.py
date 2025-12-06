from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import Rating
from app.schemas.rating import RatingCreate, RatingOut

router = APIRouter()

# 1. Baho qo‘shish
@router.post("/", response_model=RatingOut)
def add_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    existing_rating = db.query(Rating).filter_by(
        course_id=rating.course_id,
        student_id=rating.student_id
    ).first()

    if existing_rating:
        raise HTTPException(status_code=400, detail="Siz allaqachon bu kursga baho bergansiz")

    new_rating = Rating(
        course_id=rating.course_id,
        student_id=rating.student_id,
        rating_value=rating.rating_value
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

# 2. O‘rtacha reytingni ko‘rish
@router.get("/{course_id}/average")
def get_average_rating(course_id: UUID, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter_by(course_id=course_id).all()

    if not ratings:
        return {"average_rating": 0, "count": 0}

    avg = sum(r.rating_value for r in ratings) / len(ratings)
    return {"average_rating": round(avg, 2), "count": len(ratings)}
