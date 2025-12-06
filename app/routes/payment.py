from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database import get_db
from app.models.purchase import Purchase, PaymentStatus
from app.models.course import Course
from app.models.student import Student
from app.schemas.payment import TestPaymentIn


router = APIRouter(prefix="/payme", tags=["Payme (Mock)"])


@router.post("/test-pay")
def test_pay(payload: TestPaymentIn, db: Session = Depends(get_db)):
    student_id = payload.student_id
    course_id = payload.course_id

    # --- 1. Kursni tekshiramiz
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs topilmadi")

    # --- 2. Talabani tekshiramiz
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Talaba topilmadi")

    # --- 3. Agar avval sotib olgan bo‘lsa
    existing_purchase = db.query(Purchase).filter(
        Purchase.student_id == student.id,
        Purchase.course_id == course.id,
        Purchase.status == PaymentStatus.paid
    ).first()
    if existing_purchase:
        raise HTTPException(
            status_code=400,
            detail="Siz bu kursni allaqachon sotib olgansiz ✅"
        )

    # --- 4. Yangi pending purchase yozamiz
    purchase = Purchase(
        student_id=student.id,
        course_id=course.id,
        amount=course.price,
        status=PaymentStatus.pending,
        created_at=datetime.utcnow(),
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    # --- 5. Mock tarzda to‘lovni muvaffaqiyatli qilish
    purchase.status = PaymentStatus.paid
    purchase.paid_at = datetime.utcnow()

    # O‘qituvchi balansini oshiramiz
    teacher = course.teacher
    if teacher:
        teacher.balance += course.price

    db.commit()
    db.refresh(purchase)

    # --- 6. Payme API ga o‘xshash javob formati
    return {
        "success": True,
        "message": "Demo to‘lov amalga oshirildi ✅",
        "payment": {
            "id": str(purchase.id),
            "amount": purchase.amount,
            "status": purchase.status.value,
            "created_at": purchase.created_at.isoformat(),
            "paid_at": purchase.paid_at.isoformat(),
        },
        "course": {
            "id": str(course.id),
            "name": course.name,
            "price": course.price,
        },
        "student": {
            "id": str(student.id),
            "username": student.username,
            "email": student.email,
        }
    }