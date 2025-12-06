from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentOut
from app.database import get_db
from app.dependencies import get_current_user  # token validator
from app.dependencies import require_admin
from typing import List

router = APIRouter()



@router.get("/", response_model=List[StudentOut])
def get_all_students(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return db.query(Student).all()


@router.get("/{username}", response_model=StudentOut)
def get_student_by_username(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),  # ✅ endi faqat login bo'lganlar kira oladi
):
    student = db.query(Student).filter(Student.username == username).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student topilmadi.")
    return student

@router.delete("/{username}")
def delete_student_by_username(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    student = db.query(Student).filter(Student.username == username).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student topilmadi.")
    
    db.delete(student)
    db.commit()
    return {"message": f"{username} muvaffaqiyatli o‘chirildi."}


