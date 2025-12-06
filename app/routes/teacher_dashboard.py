
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherOut
from app.database import get_db
from fastapi import HTTPException
from app.dependencies import get_current_user  # token validator
from app.dependencies import require_admin

router = APIRouter()


@router.get("", response_model=List[TeacherOut])
def get_all_teachers(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return db.query(Teacher).all()


@router.get("/by-username/{username}", response_model=TeacherOut)
def get_teacher_by_username(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    teacher = db.query(Teacher).filter(Teacher.username == username).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Bunday username mavjud emas.")
    return teacher


@router.get("/by-phone/{phone_number}", response_model=TeacherOut)
def get_teacher_by_phone(
    phone_number: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    teacher = db.query(Teacher).filter(Teacher.phone_number == phone_number).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Bunday telefon raqamli teacher topilmadi.")
    return teacher


@router.delete("/by-phone/{phone_number}")
def delete_teacher_by_phone(
    phone_number: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    teacher = db.query(Teacher).filter(Teacher.phone_number == phone_number).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Bunday telefon raqamli teacher topilmadi.")
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher o‘chirildi"}