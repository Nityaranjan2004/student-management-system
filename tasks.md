# 📋 Student Management System — Master Task Checklist

This task roadmap divides the entire project into small, actionable, step-by-step tasks with clear deliverables and verification criteria.

---

## 📍 Progress Tracker Summary

| Phase | Description | Status |
| :---: | :--- | :---: |
| **Phase 1** | Foundation (Models, Schemas, Config, DB Session) | 🟢 **Done** |
| **Phase 2** | Authentication & Security (JWT, Password Hashing, User Repo, Auth Service, Endpoints) | 🟢 **Done** |
| **Phase 3** | Student Module (Repository, Service, Endpoints) | 🟢 **Done** |
| **Phase 4** | Teacher Module (Repository, Service, Endpoints) | 🟡 **Next Up** |
| **Phase 5** | Course Module (Repository, Service, Endpoints) | ⚪ Pending |
| **Phase 6** | Enrollment & Grading Module | ⚪ Pending |
| **Phase 7** | Search, Filters & Pagination Utilities | ⚪ Pending |
| **Phase 8** | Integration & Unit Tests | ⚪ Pending |
| **Phase 9** | Docker & Deployment Setup | ⚪ Pending |

---

## 🛠️ Detailed Tasks Breakdown

---

### **PHASE 1: Foundation & Infrastructure** 🟢 (COMPLETED)
- [x] **Task 1.1**: Set up project folder structure (`app/`, `alembic/`, `tests/`).
- [x] **Task 1.2**: Define SQLAlchemy Database Models in `app/models/` (`User`, `Student`, `Teacher`, `Course`, `Enrollment`).
- [x] **Task 1.3**: Create Pydantic Request & Response Schemas in `app/schemas/`.
- [x] **Task 1.4**: Configure `.env` & `app/core/config.py` for PostgreSQL and JWT secrets.
- [x] **Task 1.5**: Set up SQLAlchemy Engine & `get_db()` dependency in `app/db/session.py`.

---

### **PHASE 2: Authentication & Security Module** 🟢 (COMPLETED)
- [x] **Task 2.1: Password Hashing & JWT Utils** (`app/core/security.py`)
- [x] **Task 2.2: User Repository** (`app/repositories/user_repository.py`)
- [x] **Task 2.3: Authentication Service** (`app/services/auth_service.py`)
- [x] **Task 2.4: FastAPI Auth Dependencies & RBAC Guards** (`app/api/dependencies.py`)
- [x] **Task 2.5: Auth Endpoints** (`app/api/v1/endpoints/auth.py`, `app/api/v1/router.py`, `app/main.py`)

---

### **PHASE 3: Student Module** 🟢 (COMPLETED)
> **Goal**: Allow Admins to manage student records, and Students to view their personal profile.

- [x] **Task 3.1: Student Repository** (`app/repositories/student_repository.py`)
- [x] **Task 3.2: Student Service** (`app/services/student_service.py`)
- [x] **Task 3.3: Student Endpoints** (`app/api/v1/endpoints/students.py`)
- [x] **Task 3.4: Register in `app/api/v1/router.py`**

---

### **PHASE 4: Teacher Module** 🟡 (NEXT)
- [ ] **Task 4.1: Teacher Repository** (`app/repositories/teacher_repository.py`)
- [ ] **Task 4.2: Teacher Service** (`app/services/teacher_service.py`)
- [ ] **Task 4.3: Teacher Endpoints** (`app/api/v1/endpoints/teachers.py`)

---

### **PHASE 5: Course Module** ⚪
- [ ] **Task 5.1: Course Repository** (`app/repositories/course_repository.py`)
- [ ] **Task 5.2: Course Service** (`app/services/course_service.py`)
- [ ] **Task 5.3: Course Endpoints** (`app/api/v1/endpoints/courses.py`)

---

### **PHASE 6: Enrollment & Grading Module** ⚪
- [ ] **Task 6.1: Enrollment Repository** (`app/repositories/enrollment_repository.py`)
- [ ] **Task 6.2: Enrollment Service** (`app/services/enrollment_service.py`)
- [ ] **Task 6.3: Enrollment Endpoints** (`app/api/v1/endpoints/enrollments.py`)

---

### **PHASE 7: Search, Filters & Pagination Utilities** ⚪
- [ ] **Task 7.1**: Build generic pagination helper in `app/utils/pagination.py`.
- [ ] **Task 7.2**: Search & filter query params in Student & Course list endpoints.
- [ ] **Task 7.3**: Custom exception handlers in `app/core/exceptions.py`.

---

### **PHASE 8: Testing & Verification** ⚪
- [ ] **Task 8.1**: Pytest fixtures in `tests/conftest.py`.
- [ ] **Task 8.2**: Unit tests in `tests/unit/`.
- [ ] **Task 8.3**: Integration tests in `tests/integration/`.

---

### **PHASE 9: Docker & Deployment** ⚪
- [ ] **Task 9.1**: `Dockerfile`.
- [ ] **Task 9.2**: `docker-compose.yml`.
- [ ] **Task 9.3**: Alembic database migrations.
