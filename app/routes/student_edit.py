# from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models import Student
# from app.schemas.student import StudentUpdate, StudentOut
# from app.dependencies import get_current_user
# import uuid
# import os
# import shutil

# router = APIRouter()


# # ⚙ SETTINGS: avatar saqlanadigan papka
# UPLOAD_DIR = "static/avatars"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# # ================================================================
# #   1) Profile ma'lumotlarini o'zgartirish
# # ================================================================
# @router.put("/", response_model=StudentOut)
# def update_profile(
#     data: StudentUpdate,
#     db: Session = Depends(get_db),
#     current_user: Student = Depends(get_current_user)
# ):
#     if current_user.role != "student":
#         raise HTTPException(status_code=403, detail="Only students can update profile")
#     student = db.query(Student).filter(Student.id == current_user.id).first()
#     print(student.id)

#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")

#     # Har bir maydon berilgan bo‘lsa, o‘zgartiramiz
#     if data.full_name is not None:
#         student.full_name = data.full_name

#     if data.username is not None:
#         # Username bo'sh emasligini tekshiramiz
#         if db.query(Student).filter(Student.username == data.username, Student.id != student.id).first():
#             raise HTTPException(status_code=400, detail="Username already taken")
#         student.username = data.username

#     if data.email is not None:
#         if db.query(Student).filter(Student.email == data.email, Student.id != student.id).first():
#             raise HTTPException(status_code=400, detail="Email already taken")
#         student.email = data.email

#     if data.phone_number is not None:
#         student.phone_number = data.phone_number

#     db.commit()
#     db.refresh(student)
#     return student



# # ================================================================
# #   2) Avatar yuklash (file)
# # ================================================================
# @router.post("/avatar", response_model=StudentOut)
# def upload_avatar(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     current_user: Student = Depends(get_current_user)
# ):
#     if current_user.role != "student":
#         raise HTTPException(status_code=403, detail="Only students can upload avatars")
#     student = db.query(Student).filter(Student.id == current_user.id).first()

#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")

#     # Fayl nomini tayyorlaymiz
#     ext = file.filename.split(".")[-1]
#     avatar_name = f"{uuid.uuid4()}.{ext}"
#     avatar_path = os.path.join(UPLOAD_DIR, avatar_name)

#     # Faylni saqlaymiz
#     with open(avatar_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     # Eski avatarni o'chiramiz (agar bo'lsa)
#     if student.avatar:
#         old_path = os.path.join(UPLOAD_DIR, student.avatar)
#         if os.path.exists(old_path):
#             os.remove(old_path)

#     student.avatar = avatar_name
#     db.commit()
#     db.refresh(student)

#     return student



# # ================================================================
# #   3) Parolni o‘zgartirish (alohida endpoint – xavfsizlik uchun)
# # ================================================================
# from app.core.security import verify_password, hash_password

# class PasswordUpdate(BaseModel):
#     old_password: str
#     new_password: str


# @router.put("/change-password")
# def change_password(
#     data: PasswordUpdate,
#     db: Session = Depends(get_db),
#     current_user: Student = Depends(get_current_user)
# ):
#     if current_user.role != "student":
#         raise HTTPException(status_code=403, detail="Only students can change password")
#     student = db.query(Student).filter(Student.id == current_user.id).first()

#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")

#     # Eski parolni tekshiramiz
#     if not verify_password(data.old_password, student.hashed_password):
#         raise HTTPException(status_code=400, detail="Old password is incorrect")

#     # Yangi parolni o‘rnatamiz
#     student.hashed_password = hash_password(data.new_password)

#     db.commit()

#     return {"message": "Password updated successfully"}
