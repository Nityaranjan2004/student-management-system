from app.schemas.common import (
    BaseSchema,
    TimestampSchema,
    MessageResponse,
    DataResponse,
    PaginatedResponse,
)

from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    Token,
    TokenPayload,
    RefreshTokenRequest,
    ChangePasswordRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
)

from app.schemas.user import (
    UserRole,
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserInDB,
)

from app.schemas.student import (
    Gender,
    StudentBase,
    StudentCreate,
    StudentCreateWithUserId,
    StudentUpdate,
    StudentResponse,
    StudentDetailResponse,
)

from app.schemas.teacher import (
    TeacherBase,
    TeacherCreate,
    TeacherCreateWithUserId,
    TeacherUpdate,
    TeacherResponse,
    TeacherDetailResponse,
)

from app.schemas.course import (
    CourseBase,
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseDetailResponse,
)

from app.schemas.enrollment import (
    EnrollmentStatus,
    EnrollmentBase,
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse,
    EnrollmentDetailResponse,
)

__all__ = [
    # Common
    "BaseSchema",
    "TimestampSchema",
    "MessageResponse",
    "DataResponse",
    "PaginatedResponse",
    # Auth
    "LoginRequest",
    "RegisterRequest",
    "Token",
    "TokenPayload",
    "RefreshTokenRequest",
    "ChangePasswordRequest",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    # User
    "UserRole",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserInDB",
    # Student
    "Gender",
    "StudentBase",
    "StudentCreate",
    "StudentCreateWithUserId",
    "StudentUpdate",
    "StudentResponse",
    "StudentDetailResponse",
    # Teacher
    "TeacherBase",
    "TeacherCreate",
    "TeacherCreateWithUserId",
    "TeacherUpdate",
    "TeacherResponse",
    "TeacherDetailResponse",
    # Course
    "CourseBase",
    "CourseCreate",
    "CourseUpdate",
    "CourseResponse",
    "CourseDetailResponse",
    # Enrollment
    "EnrollmentStatus",
    "EnrollmentBase",
    "EnrollmentCreate",
    "EnrollmentUpdate",
    "EnrollmentResponse",
    "EnrollmentDetailResponse",
]
