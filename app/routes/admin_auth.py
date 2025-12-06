from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.admin import AdminCreate, AdminOut
from ..models.admin import Admin
from ..core.security import hash_password, verify_password
from ..core.security import create_access_token, create_refresh_token
from ..database import get_db

router = APIRouter()

@router.post("/register", response_model=AdminOut)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    # Check if already exists
    existing = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu admin allaqachon mavjud")

    hashed = hash_password(admin.password)
    new_admin = Admin(
        username=admin.username,
        fullname=admin.fullname,
        email=admin.email,
        hashed_password=hashed
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


@router.post("/login")
def login_admin(username: str, password: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin or not verify_password(password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Login yoki parol noto‘g‘ri")

    access_token = create_access_token(data={"sub": admin.email, "role": "admin"})
    refresh_token = create_refresh_token(data={"sub": admin.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
