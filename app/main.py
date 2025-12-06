from fastapi import FastAPI
from .database import Base, engine
from app.routes import check_token, student_auth, teacher_auth, student_dashboard, course, teacher_dashboard, admin_auth, rating, student_google_auth, teacher_google_auth, payment, category
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GeniStudy API",
    description="GeniStudy is a comprehensive platform designed to facilitate online learning and teaching. It provides a range of features for students, teachers, and administrators to manage courses, track progress, and enhance the learning experience.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_auth.router, prefix="/auth/student", tags=["Student Auth"])
app.include_router(teacher_auth.router, prefix="/auth/teacher", tags=["Teacher Auth"])

app.include_router(course.router)
app.include_router(category.router, tags=["Categories"])

app.include_router(check_token.router, tags=["Token Validation"])

app.include_router(student_dashboard.router, prefix="/dashboard/student", tags=["Student Dashboard"])
app.include_router(teacher_dashboard.router, prefix="/dashboard/teacher", tags=["Teacher Dashboard"])

app.include_router(admin_auth.router, prefix="/dashboard/admin", tags=["Admin Dashboard"])

app.include_router(rating.router, prefix="/ratings", tags=["Ratings"])

app.include_router(student_google_auth.router)
app.include_router(teacher_google_auth.router)

app.include_router(payment.router)