from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.admin import Admin
from fastapi import status
from app.models.student import Student
from app.models.teacher import Teacher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/student/login")  # yoki teacher/login




def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")   # Token ichida email saqlangan bo‘lsa
        role = payload.get("role")

        if not username or not role:
            raise HTTPException(status_code=401, detail="Token ichida username yoki role yo‘q.")

        if role == "student":
            user = db.query(Student).filter(Student.username == username).first()
        elif role == "teacher":
            user = db.query(Teacher).filter(Teacher.username == username).first()
        elif role == "admin":
            user = db.query(Admin).filter(Admin.username == username).first()
        else:
            raise HTTPException(status_code=403, detail="Noma'lum rol.")

        if user is None:
            raise HTTPException(status_code=404, detail=f"{role} topilmadi: {username}")

        user.role = role  # Role ham saqlab qo‘yilsa yaxshi (modelga bog‘lanmagan, shunchaki obyekt atributi)
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token noto‘g‘ri yoki muddati o‘tgan.")




def teacher_only(current_user = Depends(get_current_user)):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Faqat o'qituvchilar ushbu amalni bajarishi mumkin."
        )
    return current_user

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")   # Token ichida username saqlangan bo‘lsa
#         role = payload.get("role")

#         if not username or not role:
#             raise HTTPException(status_code=401, detail="Token ichida username yoki role yo‘q.")

#         if role == "student":
#             user = db.query(Student).filter(Student.username == username).first()
#         elif role == "teacher":
#             user = db.query(Teacher).filter(Teacher.username == username).first()
#         elif role == "admin":
#             user = db.query(Admin).filter(Admin.username == username).first()
#         else:
#             raise HTTPException(status_code=403, detail="Noma'lum rol.")

#         if user is None:
#             raise HTTPException(status_code=404, detail=f"{role} topilmadi: {username}")

#         user.role = role  # Role ham saqlab qo‘yilsa yaxshi (modelga bog‘lanmagan, shunchaki obyekt atributi)
#         return user

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token noto‘g‘ri yoki muddati o‘tgan.")


def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Faqat adminlar uchun ruxsat!")
    return current_user


from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
security = HTTPBearer(auto_error=False)


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    if credentials is None:
        return None  # Token jo'natilmagan, login bo'lmagan foydalanuvchi

    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if not username or not role:
            return None  # Token noto‘g‘ri, login bo‘lmagan deb hisoblaymiz

        if role == "student":
            user = db.query(Student).filter(Student.username == username).first()
        elif role == "teacher":
            user = db.query(Teacher).filter(Teacher.username == username).first()
        elif role == "admin":
            user = db.query(Admin).filter(Admin.username == username).first()
        else:
            return None  # Noma’lum role → login bo‘lmagan deb

        if user is None:
            return None  # User bazada yo‘q → login bo‘lmagan deb

        user.role = role
        return user

    except JWTError:
        return None  # Token noto‘g‘ri yoki muddati o'tgan