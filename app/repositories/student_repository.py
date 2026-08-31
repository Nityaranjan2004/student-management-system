from ast import Return
from dns.e164 import query
from struct import Struct
from typing import List,Optional
from sqlalchemy.orm import Session,joinedload
from app.models.student import Student
from app.schemas.student import StudentBase,StudentUpdate


class StudentRepository:
    def __init__(self,db:Session):
        self.db = db


def get_by_id(self,student_id:int) -> Optional[Student]:
    """Fetch student by ID with joined User relationship."""
    return(self.db.query(Student)
        .options(joinedload(Student.user))
        .filter(Student.id == student_id)
        .first()
    )


def get_by_user_id(self,user_id:int)->Optional[Student]:
    """Fetch student profile by associated User ID."""
    return(
        self.db.query(Student).
        options(joinedload(Student.user)).
        filter(Student.user_id == user_id).
        first()
    )



def get_by_roll_number(self,roll_number:str)->Optional[Student]:
    """Fetch student by unique roll number."""
    return(
        self.db.query(Student).
        filter(Student.roll_number == roll_number).first()
    )


def get_all(
        self,
        skip:int=0,
        limit:int=100,
        search:Optional[str]=None,
        grade_level:Optional[str]=None
    )->List[Student]:
    """Fetch students with search, filter, and pagination."""
    query = self.db.query(Student).options(joinedload(Student.user))
    if grade_level:
        query = query.filter(Student.grade_level == grade_level)

    if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Student.roll_number.ilike(search_filter)) |
                (Student.guardian_name.ilike(search_filter))
            )
            
    return query.count()




def create(self, student_data: StudentBase, user_id: int) -> Student:
        """Create a new student profile linked to a user."""
        db_student = Student(
            user_id=user_id,
            roll_number=student_data.roll_number,
            date_of_birth=student_data.date_of_birth,
            gender=student_data.gender,
            grade_level=student_data.grade_level,
            section=student_data.section,
            guardian_name=student_data.guardian_name,
            guardian_phone=student_data.guardian_phone,
            guardian_email=student_data.guardian_email,
            address=student_data.address
        )
        self.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student
def update(self, db_student: Student, update_data: StudentUpdate) -> Student:
        """Update an existing student profile."""
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_student, key, value)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student
def delete(self, db_student: Student) -> bool:
        """Delete student record (cascades to enrollments)."""
        self.db.delete(db_student)
        self.db.commit()
        return True