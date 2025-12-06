from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime
import requests
import os

from app.database import get_db
from app.models.student import Student
from app.core.security import create_access_token, create_refresh_token
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/students/auth/google", tags=["Google Auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")


# 1️⃣ STEP: Frontend foydalanuvchini shu linkga yo'naltiradi
@router.get("/login")
def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&scope=openid%20email%20profile"
    )
    return {"auth_url": google_auth_url}


# 2️⃣ STEP: Google qaytgach shu endpoint ishlaydi
@router.get("/callback")
def google_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="No authorization code provided")

    # Token olish
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_res = requests.post(token_url, data=token_data)
    if not token_res.ok:
        raise HTTPException(status_code=400, detail="Failed to get token from Google")

    tokens = token_res.json()
    access_token = tokens.get("access_token")

    # Foydalanuvchi ma'lumotlarini olish
    userinfo_res = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if not userinfo_res.ok:
        raise HTTPException(status_code=400, detail="Failed to get user info")

    user_info = userinfo_res.json()

    email = user_info["email"]
    full_name = user_info.get("name")
    username = email.split("@")[0]

    # Baza tekshirish
    student = db.query(Student).filter(Student.email == email).first()
    if not student:
        student = Student(
            full_name=full_name,
            username=username,
            email=email,
            hashed_password=None  # Google foydalanuvchilarda parol yo‘q
        )
        db.add(student)
        db.commit()
        db.refresh(student)

    # Tokenlar yaratish
    access_token_jwt = create_access_token({"sub": student.username, "role": "student"})
    refresh_token_jwt = create_refresh_token({"sub": student.username, "role": "student"})

    return {
        "message": "Google login successful",
        "student_id": student.id,
        "access_token": access_token_jwt,
        "refresh_token": refresh_token_jwt,
        "token_type": "bearer"
    }
