from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random, string

from app.database import get_db
from app.models.teacher import Teacher
from app.models.verification import VerificationCodeTeacher as VerificationCode
from app.schemas.teacher import TeacherRegister, TeacherVerify, TeacherLogin
from app.core.security import hash_password
from app.core.email import send_verification_email
from app.core.security import create_access_token, create_refresh_token, verify_password

router = APIRouter(
    tags=["Teacher Auth"]
)

@router.post("/register")
def register_teacher(data: TeacherRegister, db: Session = Depends(get_db)):
    # Check for duplicates
    if db.query(Teacher).filter(Teacher.email == data.email).first():
        raise HTTPException(status_code=400, detail="Bu email allaqachon ro‘yxatdan o‘tgan.")
    if db.query(Teacher).filter(Teacher.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username band.")
    # if db.query(Teacher).filter(Teacher.phone_number == data.phone_number).first():
    #     raise HTTPException(status_code=400, detail="Telefon raqam band.")

    # Kod yaratish
    code = ''.join(random.choices(string.digits, k=6))
    hashed_pw = hash_password(data.password)

    # VerificationCode yozish
    verify = VerificationCode(
        email=data.email,
        full_name=data.fullname,
        username=data.username,
        # phone_number=data.phone_number,
        hashed_password=hashed_pw,
        code=code
    )
    db.add(verify)
    db.commit()

    # Email yuborish
    # send_verification_email(data.email, code)
    print(f"Verification code sent to {data.email}: {code}")

    return {"message": f"Tasdiqlash kodingiz emailga yuborildi: {code}"}

@router.post("/verify")
def verify_teacher(data: TeacherVerify, db: Session = Depends(get_db)):
    record = db.query(VerificationCode).filter(
        VerificationCode.email == data.email,
        VerificationCode.code == data.code
    ).first()

    if not record:
        raise HTTPException(status_code=400, detail="Kod noto‘g‘ri yoki email topilmadi.")

    # Teacher yaratish
    teacher = Teacher(
        fullname=record.full_name,
        username=record.username,
        email=record.email,
        # phone_number=record.phone_number,
        hashed_password=record.hashed_password
        # birthday=data.birthday  # faqat verify paytida yuboriladi
    )
    db.add(teacher)
    db.delete(record)
    db.commit()

    return {"message": "Ro‘yxatdan o‘tish muvaffaqiyatli tugadi 🎉"}





@router.post("/login")
def login_teacher(data: TeacherLogin, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(
        Teacher.username == data.username,
        # Teacher.phone_number == data.phone_number
    ).first()

    if not teacher:
        raise HTTPException(status_code=401, detail="Foydalanuvchi topilmadi.")

    if not verify_password(data.password, teacher.hashed_password):
        raise HTTPException(status_code=401, detail="Parol noto‘g‘ri.")

    access_token = create_access_token(data={"sub": teacher.email, "role": "teacher"})
    refresh_token = create_refresh_token(data={"sub": teacher.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "teacher": {
            "id": teacher.id,
            "fullname": teacher.fullname,
            "username": teacher.username,
            "email": teacher.email,
            "phone_number": teacher.phone_number
        }
    }