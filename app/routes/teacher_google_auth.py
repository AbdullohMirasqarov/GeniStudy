import requests
from fastapi import Request
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.teacher import Teacher
from app.core.security import create_access_token, create_refresh_token
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/teachers/auth/google", tags=["Google Auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI_TEACHER")

@router.get("/login")
def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
        "&access_type=offline"
    )
    return {"auth_url": google_auth_url}


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
        raise HTTPException(status_code=400, detail=f"Failed to get token: {token_res.text}")

    tokens = token_res.json()
    access_token = tokens.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="Access token not found")

    # Google foydalanuvchi ma'lumotlarini olish
    userinfo_res = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if not userinfo_res.ok:
        raise HTTPException(status_code=400, detail=f"Failed to get user info: {userinfo_res.text}")

    user_info = userinfo_res.json()
    email = user_info.get("email")
    fullname = user_info.get("name")
    username = email.split("@")[0] if email else None

    if not email:
        raise HTTPException(status_code=400, detail="Email not found in Google data")

    # Bazada bor-yo‘qligini tekshirish
    teacher = db.query(Teacher).filter(Teacher.email == email).first()

    if not teacher:
        teacher = Teacher(
            fullname=fullname or username,
            username=username,
            email=email,
            hashed_password=None,
            is_verified=True,
        )
        db.add(teacher)
        db.commit()
        db.refresh(teacher)

    # JWT token yaratish
    access_token_jwt = create_access_token({"sub": teacher.username, "role": "teacher"})
    refresh_token_jwt = create_refresh_token({"sub": teacher.username, "role": "teacher"})

    return {
        "message": "Google login successful",
        "teacher": {
            "id": str(teacher.id),
            "fullname": teacher.fullname,
            "email": teacher.email,
            "username": teacher.username
        },
        "access_token": access_token_jwt,
        "refresh_token": refresh_token_jwt,
        "token_type": "bearer"
    }
