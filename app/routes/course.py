from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.course import Course
from app.models.purchase import PaymentStatus
from app.models.teacher import Teacher
from app.schemas.course import CourseCreate, CourseUpdate, CourseOut
from app.dependencies import get_current_user
import os
import shutil
import uuid
import json
from app.models.video import Video
from fastapi import File, UploadFile, Form
from app.models.teacher import Teacher
from ..cloudinary_setup import cloudinary
from uuid import UUID
from app.schemas.course import CoursePreview

from app.bunnycdn_setup import BUNNY_CDN_URL
from app.bunny_uploader import upload_to_bunnycdn
from app.schemas.course import CourseOutWithoutVideos
from app.dependencies import get_current_user_optional
from app.models.purchase import Purchase

from app.models.course import CourseCategory, CourseSubCategory
from app.schemas.course import CourseOut, CourseOutWithoutVideos
from typing import Optional



router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)





# @router.post("/")
# def create_course_to_db(
#     name: str = Form(...),
#     description: str = Form(""),
#     price: int = Form(...),
#     photo: UploadFile = File(...),
#     videos: list[UploadFile] = File([]),
#     video_titles: list[str] = Form(...),
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     # 1. Teacher tekshiruv
#     teacher = db.query(Teacher).filter(Teacher.email == current_user.email).first()
#     if not teacher:
#         raise HTTPException(status_code=403, detail="Faqat teacherlar kurs yarata oladi.")

#     # 2. Rasmni Cloudinary ga yuklash
#     image_result = cloudinary.uploader.upload(photo.file, folder="courses/images")

#     # 3. Course yaratish (image_data o‘rniga image_url bo‘ladi)
#     course = Course(
#         name=name,
#         description=description,
#         price=price,
#         teacher_id=teacher.id,
#         image_url=image_result["secure_url"]  # <-- yangi
#     )
#     db.add(course)
#     db.commit()
#     db.refresh(course)

#     if len(video_titles) != len(videos):
#         raise HTTPException(status_code=400, detail="Videolar soni va title'lar soni mos kelmayapti.")

#     for i, video in enumerate(videos):
#         result = cloudinary.uploader.upload(
#             video.file,
#             resource_type="video",
#             folder="courses/videos"
#         )
#         db.add(Video(
#             title=video_titles[i],  # <-- userdan kelgan title
#             order=i + 1,
#             video_url=result["secure_url"],
#             course_id=course.id
#         ))

#     db.commit()

#     # return {"message": "Kurs Cloudinary'ga yuklandi!", "course_id": course.id}

#     return {"message": "Kurs rasm va videolari bilan Cloudinary'ga yuklandi!", "course_id": course.id}


# @router.post("/")
# def create_course_to_db(
#     name: str = Form(...),
#     description: str = Form(""),
#     price: int = Form(...),
#     photo: UploadFile = File(...),
#     videos: list[UploadFile] = File([]),
#     video_titles: list[str] = Form(...),
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     # 1. Teacher tekshiruv
#     teacher = db.query(Teacher).filter(Teacher.email == current_user.email).first()
#     if not teacher:
#         raise HTTPException(status_code=403, detail="Faqat ustozlar kurs yarata oladi.")

#     # 2. Rasmni Cloudinary ga yuklash
#     image_result = cloudinary.uploader.upload(photo.file, folder="courses/images")

#     # 3. Course yaratish
#     course = Course(
#         name=name,
#         description=description,
#         price=price,
#         teacher_id=teacher.id,
#         image_url=image_result["secure_url"]
#     )
#     db.add(course)
#     db.commit()
#     db.refresh(course)

#     if len(video_titles) != len(videos):
#         raise HTTPException(status_code=400, detail="Videolar soni va title'lar soni mos kelmayapti.")

#     # 4. Videolarni BunnyCDN ga yuklash
#     for i, video in enumerate(videos):
#         video_bytes = video.file.read()
#         filename = f"courses_videos/{course.id}_{i}_{video.filename}"

#         success, message = upload_to_bunnycdn(filename, video_bytes)
#         if not success:
#             raise HTTPException(status_code=500, detail=message)

#         full_url = f"{BUNNY_CDN_URL}/{filename}"

#         db.add(Video(
#             title=video_titles[i],
#             order=i + 1,
#             video_url=full_url,
#             course_id=course.id
#         ))

#     db.commit()

#     return {"message": "Kurs rasm va videolari yuklandi!", "course_id": course.id}



@router.post("/")
def create_course_to_db(
    name: str = Form(...),
    description: str = Form(""),
    price: int = Form(...),

    category_id: UUID = Form(...),
    subcategory_id: Optional[UUID] = Form(None),

    photo: UploadFile = File(...),
    videos: list[UploadFile] = File([]),
    video_titles: list[str] = Form(...),

    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Teacher tekshiruv
    teacher = db.query(Teacher).filter(Teacher.email == current_user.email).first()
    if not teacher:
        raise HTTPException(status_code=403, detail="Faqat ustozlar kurs yarata oladi.")

    # 2. Category tekshiruv
    category = db.query(CourseCategory).filter(CourseCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category topilmadi.")

    # 3. Subcategory tekshiruv
    if subcategory_id:
        subcat = db.query(CourseSubCategory).filter(
            CourseSubCategory.id == subcategory_id,
            CourseSubCategory.category_id == category_id
        ).first()
        if not subcat:
            raise HTTPException(
                status_code=400,
                detail="Subcategory shu kategoriyaga tegishli emas!"
            )

    # 4. Rasmni Cloudinary ga yuklash
    try:
        image_result = cloudinary.uploader.upload(photo.file, folder="courses/images")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rasm yuklashda xatolik: {str(e)}")

    # 5. Course yaratish
    course = Course(
        name=name,
        description=description,
        price=price,
        teacher_id=teacher.id,
        image_url=image_result["secure_url"],
        category_id=category_id,
        subcategory_id=subcategory_id
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    # 6. Videolar validatsiyasi
    if len(video_titles) != len(videos):
        raise HTTPException(status_code=400, detail="Videolar soni va title soni mos emas.")

    # 7. Videolarni BunnyCDN ga yuklash
    for i, video in enumerate(videos):
        video_bytes = video.file.read()
        filename = f"courses_videos/{course.id}_{i}_{video.filename}"

        success, message = upload_to_bunnycdn(filename, video_bytes)
        if not success:
            raise HTTPException(status_code=500, detail=message)

        full_url = f"{BUNNY_CDN_URL}/{filename}"

        db.add(Video(
            title=video_titles[i],
            order=i + 1,
            video_url=full_url,
            course_id=course.id
        ))

    db.commit()

    return {"message": "Kurs muvaffaqiyatli yaratildi!", "course_id": course.id}




@router.get("/", response_model=list[CourseOut])
def get_all_courses_only_for_admins(db: Session = Depends(get_db)):
    return db.query(Course).all()


@router.get("/preview", response_model=list[CoursePreview])
def get_all_courses_preview(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return [CoursePreview(id=c.id, name=c.name, image_url=c.image_url) for c in courses]




# @router.get("/{course_id}", response_model=CourseOut)
# def get_course(course_id: str, db: Session = Depends(get_db)):
#     course = db.query(Course).filter(Course.id == course_id).first()
#     if not course:
#         raise HTTPException(status_code=404, detail="Kurs topilmadi.")
#     return course





@router.get("/my-courses", response_model=list[CourseOut])
def get_my_courses(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Foydalanuvchining o‘z kurslarini qaytaradi:
    - student → sotib olgan kurslar
    - teacher → yaratgan kurslar
    - admin → barcha kurslar
    """
    if current_user.role == "student":
        purchases = (
            db.query(Purchase)
            .filter(
                Purchase.student_id == current_user.id,
                Purchase.status == PaymentStatus.paid
            )
            .all()
        )
        course_ids = [p.course_id for p in purchases]
        courses = db.query(Course).filter(Course.id.in_(course_ids)).all()

    elif current_user.role == "teacher":
        courses = db.query(Course).filter(Course.teacher_id == current_user.id).all()

    elif current_user.role == "admin":
        courses = db.query(Course).all()

    else:
        raise HTTPException(status_code=403, detail="Ruxsat etilmagan foydalanuvchi turi.")

    return courses








@router.get("/{course_id}", response_model=CourseOut)
def get_course(
    course_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_optional),  # bu optional bo‘lishi kerak
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs topilmadi.")

    # Agar foydalanuvchi login qilmagan bo‘lsa → videolarsiz ma'lumot
    if not current_user:
        print("User login qilmagan")
        return CourseOutWithoutVideos.model_validate(course)


    # Foydalanuvchi sotib olganmi?
    purchase = db.query(Purchase).filter(
        Purchase.student_id == current_user.id,
        Purchase.course_id == course.id,
        Purchase.status == PaymentStatus.paid
    ).first()

    # Agar sotib olgan bo‘lsa → to‘liq (videolar bilan)
    if purchase:
        print("User sotib olgan")
        return CourseOut.model_validate(course)

    # Aks holda videolarsiz
    print("User sotib olmagan")
    return CourseOutWithoutVideos.model_validate(course)









@router.put("/{course_id}", response_model=CourseOut)
def update_course(course_id: str, data: CourseUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs topilmadi.")

    teacher = db.query(Teacher).filter(Teacher.email == current_user.email).first()

    if not teacher or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Faqat o'z kursingizni tahrirlash mumkin.")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)
    return course


# @router.delete("/{course_id}")
# def delete_course(course_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     course = db.query(Course).filter(Course.id == course_id).first()
#     if not course:
#         raise HTTPException(status_code=404, detail="Kurs topilmadi.")

#     teacher = db.query(Teacher).filter(Teacher.email == current_user.email).first()

#     if not teacher or course.teacher_id != teacher.id:
#         raise HTTPException(status_code=403, detail="Faqat o'z kursingizni o'chira olasiz.")

#     db.delete(course)
#     db.commit()
#     return {"message": "Kurs muvaffaqiyatli o'chirildi."}


@router.delete("/{course_id}")
def delete_course(course_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs topilmadi.")

    teacher = db.query(Teacher).filter(Teacher.email == current_user.email).first()

    if not teacher or course.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Faqat o'z kursingizni o'chira olasiz.")

    db.delete(course)
    db.commit()
    return {"message": "Kurs muvaffaqiyatli o‘chirildi."}



