from fastapi import APIRouter, Depends
from app.dependencies import get_current_user  # token validator
router = APIRouter(prefix="/get", tags=["Get Me"])

@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    """
    Foydalanuvchining o'z ma'lumotlarini qaytaradi.
    Student → Student modeli bo'yicha
    Teacher → Teacher modeli bo'yicha
    Admin → Admin modeli bo'yicha
    """
    return current_user


