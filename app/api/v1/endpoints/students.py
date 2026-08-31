from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.student import StudentCreate, StudentCreateWithUserId, StudentUpdate, StudentResponse
from app.schemas.common import MessageResponse
from app.models.user import User
from app.services.student_service import StudentService
from app.api.dependencies import require_admin, require_teacher, require_student, get_current_active_user

router = APIRouter()


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreate,
    current_admin: User = Depends(require_admin),  # 🔒 Only ADMIN
    db: Session = Depends(get_db)
):
    """Admin creates a new Student profile along with a new User account."""
    service = StudentService(db)
    return service.create_student_with_account(payload)


@router.post("/link-user", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student_profile(
    payload: StudentCreateWithUserId,
    current_admin: User = Depends(require_admin),  # 🔒 Only ADMIN
    db: Session = Depends(get_db)
):
    """Admin links a Student profile to an existing User ID."""
    service = StudentService(db)
    return service.create_student_for_user(payload)


@router.get("/", response_model=List[StudentResponse])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None, description="Search by roll number or guardian name"),
    grade_level: Optional[str] = Query(None, description="Filter by grade level"),
    current_user: User = Depends(require_teacher),  # 🔒 ADMIN or TEACHER
    db: Session = Depends(get_db)
):
    """List and search students (Admin & Teachers)."""
    service = StudentService(db)
    return service.get_all_students(skip=skip, limit=limit, search=search, grade_level=grade_level)


@router.get("/me", response_model=StudentResponse)
def get_my_student_profile(
    current_user: User = Depends(require_student),  # 🔒 Logged in STUDENT
    db: Session = Depends(get_db)
):
    """Get the profile of the currently logged-in student."""
    service = StudentService(db)
    return service.get_student_by_user_id(current_user.id)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student_details(
    student_id: int,
    current_user: User = Depends(get_current_active_user),  # 🔒 Authenticated Users
    db: Session = Depends(get_db)
):
    """Get student details by student ID."""
    service = StudentService(db)
    return service.get_student_by_id(student_id)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    current_admin: User = Depends(require_admin),  # 🔒 Only ADMIN
    db: Session = Depends(get_db)
):
    """Update student profile details (Admin only)."""
    service = StudentService(db)
    return service.update_student(student_id, payload)


@router.delete("/{student_id}", response_model=MessageResponse)
def delete_student(
    student_id: int,
    current_admin: User = Depends(require_admin),  # 🔒 Only ADMIN
    db: Session = Depends(get_db)
):
    """Delete a student and their user account (Admin only)."""
    service = StudentService(db)
    service.delete_student(student_id)
    return MessageResponse(message="Student deleted successfully.")
