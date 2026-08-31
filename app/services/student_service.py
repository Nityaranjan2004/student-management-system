from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.student import Student
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.student import StudentCreate, StudentCreateWithUserId, StudentUpdate
from app.schemas.user import UserRole
from app.core.security import get_password_hash


class StudentService:
    def __init__(self, db: Session):
        self.db = db
        self.student_repo = StudentRepository(db)
        self.user_repo = UserRepository(db)

    def create_student_with_account(self, data: StudentCreate) -> Student:
        """Admin creates a Student Profile + New User Account together."""
        # 1. Check if email already registered
        if self.user_repo.get_by_email(data.user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )

        # 2. Check if username already taken
        if self.user_repo.get_by_username(data.user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists."
            )

        # 3. Check if roll number is already used
        if self.student_repo.get_by_roll_number(data.roll_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A student with this roll number already exists."
            )

        # 4. Create User Account with role STUDENT
        hashed_password = get_password_hash(data.user.password)
        data.user.role = UserRole.STUDENT
        user = self.user_repo.create(data.user, hashed_password)

        # 5. Create Student profile linked to user.id
        return self.student_repo.create(data, user_id=user.id)

    def create_student_for_user(self, data: StudentCreateWithUserId) -> Student:
        """Create a student profile for an existing user account."""
        user = self.user_repo.get_by_id(data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        if self.student_repo.get_by_user_id(data.user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This user already has a student profile."
            )

        if self.student_repo.get_by_roll_number(data.roll_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Roll number already in use."
            )

        return self.student_repo.create(data, user_id=data.user_id)

    def get_student_by_id(self, student_id: int) -> Student:
        """Fetch student profile by ID."""
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found."
            )
        return student

    def get_student_by_user_id(self, user_id: int) -> Student:
        """Fetch student profile for logged-in student user."""
        student = self.student_repo.get_by_user_id(user_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found for this user."
            )
        return student

    def get_all_students(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        grade_level: Optional[str] = None
    ) -> List[Student]:
        """Fetch list of students."""
        return self.student_repo.get_all(skip=skip, limit=limit, search=search, grade_level=grade_level)

    def update_student(self, student_id: int, update_data: StudentUpdate) -> Student:
        """Update student details."""
        student = self.get_student_by_id(student_id)

        # If updating roll number, verify it's not taken by another student
        if update_data.roll_number and update_data.roll_number != student.roll_number:
            if self.student_repo.get_by_roll_number(update_data.roll_number):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Roll number already in use by another student."
                )

        return self.student_repo.update(student, update_data)

    def delete_student(self, student_id: int) -> bool:
        """Delete student and their user account."""
        student = self.get_student_by_id(student_id)
        # Deleting the student profile
        self.student_repo.delete(student)
        # Also clean up the user login account
        if student.user:
            self.user_repo.delete(student.user)
        return True
