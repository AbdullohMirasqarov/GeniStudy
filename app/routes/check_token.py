
from fastapi import APIRouter
from fastapi import Depends
from app.dependencies import get_current_user


router = APIRouter()

@router.get("/auth/me")
def read_users_me(current_user=Depends(get_current_user)):
    return {
        "role": current_user.role,
        "is_valid": True
    }