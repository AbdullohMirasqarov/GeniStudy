from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.email import send_verification_email
from ..schemas.student import StudentCreate, CodeVerify, StudentLogin
from ..models.student import Student
from ..models.verification import VerificationCodeStudent as VerificationCode
from ..database import get_db
from ..core.security import hash_password, create_access_token, create_refresh_token, verify_password
from datetime import datetime, timedelta
import random

router = APIRouter()



@router.post("/register")
def register(data: StudentCreate, db: Session = Depends(get_db)):
    existing_student = db.query(Student).filter((Student.email == data.email) | (Student.username == data.username)).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="User already exists")

    code = str(random.randint(100000, 999999))
    hashed_pw = hash_password(data.password)

    verification = db.query(VerificationCode).filter_by(email=data.email).first()
    if verification:
        verification.code = code
        verification.full_name = data.full_name
        verification.username = data.username
        # verification.phone_number = data.phone_number
        verification.hashed_password = hashed_pw
        verification.created_at = datetime.utcnow()
    else:
        verification = VerificationCode(
            email=data.email,
            code=code,
            full_name=data.full_name,
            username=data.username,
            # phone_number=data.phone_number,
            hashed_password=hashed_pw
        )
        db.add(verification)

    db.commit()
    # send_verification_email(data.email, code)
    print(f"Verification code sent to {data.email}: {code}")  # For debugging purposes
    return {"message": f"Verification code sent to {code}"}

@router.post("/verify")
def verify_code(data: CodeVerify, db: Session = Depends(get_db)):
    verification = db.query(VerificationCode).filter_by(email=data.email).first()
    if not verification or verification.code != data.code:
        raise HTTPException(status_code=400, detail="Invalid code")

    if (datetime.utcnow() - verification.created_at) > timedelta(minutes=4):
        raise HTTPException(status_code=400, detail="Code expired")

    student = Student(
        full_name=verification.full_name,
        username=verification.username,
        email=verification.email,
        # phone_number=verification.phone_number,
        hashed_password=verification.hashed_password
    )
    db.add(student)
    db.delete(verification)
    db.commit()
    db.refresh(student)

    access_token = create_access_token({"sub": student.username, "role": "student"})
    refresh_token = create_refresh_token({"sub": student.username})

    return {
        "message": "Registration complete",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }





@router.post("/login")
def login(data: StudentLogin, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.username == data.username).first()
    if not student:
        raise HTTPException(status_code=400, detail="Username not found")
    if not verify_password(data.password, student.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token({"sub": student.username,  "role": "student"})
    refresh_token = create_refresh_token({"sub": student.username, "role": "student"})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }