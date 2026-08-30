# 🎓 Student Management System — Project & Business Flow

This document details the complete end-to-end business logic, user flows, database architecture, API routing design, and backend request processing pipeline for the **Student Management System**.

---

## 👥 1. The 3 Main System Roles

```
                 STUDENT MANAGEMENT SYSTEM
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
          ADMIN           TEACHER          STUDENT
```

---

## 🔐 2. User Registration & Login Flow

```
User
  │
  ▼
Register (Email + Username + Password + Role)
  │
  ▼
Password Hashing (Bcrypt)
  │
  ▼
Save to PostgreSQL (users table)
  │
  ▼
Login (Username/Email + Password)
  │
  ▼
JWT Access Token Generated
  │
  ▼
Client attaches to all future requests:
Header: Authorization: Bearer <token>
```

---

## 🛡️ 3. Role-Based Flow Charts

### 3.1. 👑 ADMIN Flow
The Admin manages the entire institution:

```
ADMIN
  │
  ├── Manage Students
  │      ├── Create (POST /api/v1/students)
  │      ├── View All (GET /api/v1/students)
  │      ├── View Single (GET /api/v1/students/{id})
  │      ├── Update (PUT /api/v1/students/{id})
  │      └── Delete (DELETE /api/v1/students/{id})
  │
  ├── Manage Teachers
  │      ├── Create (POST /api/v1/teachers)
  │      ├── View All (GET /api/v1/teachers)
  │      ├── View Single (GET /api/v1/teachers/{id})
  │      ├── Update (PUT /api/v1/teachers/{id})
  │      └── Delete (DELETE /api/v1/teachers/{id})
  │
  ├── Manage Courses
  │      ├── Create (POST /api/v1/courses)
  │      ├── Assign Teacher (PUT /api/v1/courses/{id})
  │      ├── View All (GET /api/v1/courses)
  │      └── Delete (DELETE /api/v1/courses/{id})
  │
  └── Manage Enrollments
         ├── View All (GET /api/v1/enrollments)
         └── Admin Override / Force Drop
```

---

### 3.2. 🎓 STUDENT Flow
A student logs in, views catalog, and manages course enrollments:

```
STUDENT
   │
   ▼
Login ➔ JWT Token (Role: STUDENT)
   │
   ├──→ View Profile (GET /api/v1/students/me)
   │
   ├──→ View Available Courses (GET /api/v1/courses)
   │
   ├──→ Self-Enroll in Course (POST /api/v1/enrollments)
   │
   ├──→ View My Enrolled Courses (GET /api/v1/enrollments/me)
   │
   └──→ View My Grades & Academic Record
```

**Example Scenario:**
1. Student logs in.
2. Calls `GET /courses` ➔ Sees `"Python Programming" (ID: 10)`.
3. Calls `POST /enrollments` with `{"course_id": 10}`.
4. Enrollment is recorded with status `ENROLLED`.

---

### 3.3. 👨‍🏫 TEACHER Flow
A teacher logs in, manages assigned courses, and assigns grades:

```
TEACHER
   │
   ▼
Login ➔ JWT Token (Role: TEACHER)
   │
   ├──→ View Profile (GET /api/v1/teachers/me)
   │
   ├──→ View Assigned Courses (GET /api/v1/teachers/me/courses)
   │
   ├──→ View Enrolled Students (GET /api/v1/courses/{course_id}/students)
   │
   └──→ Manage Grades & Status (PUT /api/v1/enrollments/{enrollment_id}/grade)
```

**Example Scenario:**
1. Teacher Rahul logs in.
2. Calls `GET /teachers/me/courses` ➔ Sees assigned course `"Python Programming"`.
3. Calls `GET /courses/10/students` ➔ Sees enrolled students (`Nitya`, `Alex`, etc.).
4. Submits grade: `PUT /enrollments/50/grade` with `{"grade": "A", "status": "completed"}`.

---

## 🔄 4. Course & Enrollment Relationship Flow

```
              COURSE
                ▲
                │
           ENROLLMENT (Bridge Table)
                │
                ▼
             STUDENT
```

- **A Student can enroll in many Courses**:
  ```
  Student (Nitya) ───┬───> Python Programming
                     ├───> Database Management
                     └───> Web Development
  ```

- **A Course has many Students**:
  ```
  Python Programming ───┬───> Student A
                        ├───> Student B
                        ├───> Student C
                        └───> Student D
  ```

- **Central Link**:
  $$\text{Student } \longleftrightarrow \text{ Enrollment } \longleftrightarrow \text{ Course}$$

---

## 🏆 5. Grading Flow

```
Student ───> Enrollment ───> Course ───> Teacher ───> Assign Grade
```

```
Python Programming (Course)
       │
       ▼
    Student (Nitya)
       │
       ▼
     87 marks
       │
       ▼
     Grade: A
```
- The teacher enters the grade.
- The student can immediately view the grade on their portal.

---

## 🔍 6. Search, Filter & Pagination Flow

### 6.1. Search & Filter
- Search students: `GET /api/v1/students?search=nitya`
- Filter students by grade/department: `GET /api/v1/students?department=CSE`
- Search courses: `GET /api/v1/courses?search=python`
- Filter courses by teacher: `GET /api/v1/courses?teacher_id=5`

### 6.2. Pagination Flow
```
10,000 Total Students in PostgreSQL
                │
                ▼
Client sends: GET /students?page=1&limit=20
                │
                ▼
SQLAlchemy applies: .offset(0).limit(20)
                │
                ▼
FastAPI returns: 20 records + pagination metadata (total, total_pages, has_next)
```

---

## 🌐 7. Complete Business Flow Overview

```
                         ┌──────────────┐
                         │     USER     │
                         └──────┬───────┘
                                │
                          Register/Login
                                │
                                ▼
                         ┌──────────────┐
                         │  JWT Token   │
                         └──────┬───────┘
                                │
                     ┌──────────┼──────────┐
                     ▼          ▼          ▼
                   ADMIN      TEACHER    STUDENT
                     │          │          │
          ┌──────────┼───┐      │          │
          ▼          ▼   ▼      ▼          ▼
       Students   Teachers Courses     View Courses
                              │          │
                              │          ▼
                              │       Enroll
                              │          │
                              └────┬─────┘
                                   ▼
                              Enrollment
                                   │
                                   ▼
                                 Grades
                                   │
                                   ▼
                              Student View
```

---

## 🗄️ 8. Database Cardinality & Relationships

```
                    USERS (Auth)
                      │
             ┌────────┴────────┐
             ▼                 ▼
          STUDENTS          TEACHERS
      (1:1 with User)    (1:1 with User)
             │                 │
             │                 ▼
             │              COURSES (1:N from Teacher)
             │                 │
             │                 │
             └── ENROLLMENTS ──┘
             (N:M Junction Table)
```

- **`User ↔ Student`**: `1 : 1` (`students.user_id ➔ users.id`)
- **`User ↔ Teacher`**: `1 : 1` (`teachers.user_id ➔ users.id`)
- **`Teacher ↔ Course`**: `1 : N` (`courses.teacher_id ➔ teachers.id`)
- **`Student ↔ Course`**: `N : M` (Connected via `enrollments` table with `student_id` & `course_id`)

---

## 🛣️ 9. API Endpoint Structure (`/api/v1`)

```
/api/v1
│
├── /auth
│   ├── POST /register        (Public self-registration)
│   ├── POST /login           (Returns JWT token)
│   ├── POST /refresh         (Renew expired access token)
│   └── GET  /me              (Get current authenticated user profile)
│
├── /students
│   ├── POST   /              (Admin: Register new student)
│   ├── GET    /              (Admin/Teacher: List & Search students with pagination)
│   ├── GET    /me            (Student: Get personal academic profile)
│   ├── GET    /{id}          (Admin/Teacher: Get student details)
│   ├── PUT    /{id}          (Admin: Update student details)
│   └── DELETE /{id}          (Admin: Delete student record)
│
├── /teachers
│   ├── POST   /              (Admin: Register new teacher)
│   ├── GET    /              (Admin: List & Search teachers)
│   ├── GET    /me            (Teacher: Get personal profile)
│   ├── GET    /{id}          (Admin: Get teacher details)
│   ├── PUT    /{id}          (Admin: Update teacher details)
│   └── DELETE /{id}          (Admin: Delete teacher record)
│
├── /courses
│   ├── POST   /              (Admin: Create new course)
│   ├── GET    /              (Public/All: List available courses)
│   ├── GET    /{id}          (Public/All: Course details + teacher info)
│   ├── PUT    /{id}          (Admin: Update course details/assigned teacher)
│   └── DELETE /{id}          (Admin: Delete course)
│
└── /enrollments
    ├── POST   /              (Student/Admin: Enroll in a course)
    ├── GET    /              (Admin: View all enrollments)
    ├── GET    /me            (Student: View my enrolled courses & grades)
    ├── PUT    /{id}/grade    (Teacher/Admin: Update grade / completion status)
    └── DELETE /{id}          (Student/Admin: Drop enrollment)
```

---

## ⚙️ 10. Backend Request Processing Pipeline

For **every incoming API request**, the backend executes this robust pipeline:

```
HTTP Request (Client)
     │
     ▼
FastAPI Router & CORS Middleware
     │
     ▼
Authentication Guard (Verify JWT Signature & Expiration)
     │
     ▼
Authorization Guard (Verify User Role: ADMIN, TEACHER, STUDENT)
     │
     ▼
Pydantic Schema Validation (Validate body/query data types & constraints)
     │
     ▼
Service Layer (Execute business rules, conflict checks, password hashing)
     │
     ▼
Repository Layer (Construct SQLAlchemy queries)
     │
     ▼
PostgreSQL Database (Execute SQL Transaction)
     │
     ▼
Repository Layer (Receive ORM entities)
     │
     ▼
Service Layer (Process data & business logic)
     │
     ▼
Response Pydantic Schema (Filter out private fields like password hashes)
     │
     ▼
HTTP Response (JSON to Client with status code 200/201/400/401/403/404)
```

### 💡 Concrete Request Example: `POST /enrollments`

```
1. Client sends: POST /api/v1/enrollments {"course_id": 10} with Bearer Token
2. Auth Guard: Validates JWT token ➔ Extracts user_id & role
3. Role Guard: Confirms user role is STUDENT
4. Request Validation: Confirms course_id is a positive integer
5. Service Rule 1: Checks if course_id (10) exists and is_active=True
6. Service Rule 2: Checks if student is already enrolled in course 10 (prevent duplicates)
7. Repository: Executes INSERT INTO enrollments (student_id, course_id, status)
8. PostgreSQL: Saves record and assigns new enrollment ID
9. Response: Serializes into EnrollmentResponse schema ➔ Returns HTTP 201 Created
```

---

## 🏗️ 11. Complete Project in One Picture

```
                         STUDENT MANAGEMENT SYSTEM
                                     │
                   ┌─────────────────┼─────────────────┐
                   ▼                 ▼                 ▼
                 ADMIN            TEACHER            STUDENT
                   │                 │                 │
            ┌──────┼──────┐          │          ┌──────┼──────┐
            ▼      ▼      ▼          ▼          ▼      ▼      ▼
         Students Teachers Courses   Grades   Profile Courses Enroll
            │      │      │          ▲                 │
            │      │      └──────────┘                 │
            │      │                                   │
            └──────┴───────────────┬───────────────────┘
                                   │
                                   ▼
                              ENROLLMENTS
                                   │
                                   ▼
                              DATABASE
                                   │
                                   ▼
                              PostgreSQL
```

---

## 🎯 12. Recommended Step-by-Step Build Order

1. **FastAPI Setup** (App configuration & CORS)
2. **Database Engine** (SQLAlchemy `session.py` with PostgreSQL connection pool)
3. **Base & TimestampMixin** (`app/db/base.py`)
4. **User & Auth Models** (`app/models/user.py`)
5. **Security & JWT** (`app/core/security.py` — Bcrypt & PyJWT)
6. **Auth Flow** (`UserRepository` ➔ `AuthService` ➔ `/api/v1/endpoints/auth.py`)
7. **Student Module** (`StudentRepository` ➔ `StudentService` ➔ `/students` endpoints)
8. **Teacher Module** (`TeacherRepository` ➔ `TeacherService` ➔ `/teachers` endpoints)
9. **Course Module** (`CourseRepository` ➔ `CourseService` ➔ `/courses` endpoints)
10. **Enrollment & Grades Module** (`EnrollmentRepository` ➔ `EnrollmentService` ➔ `/enrollments` endpoints)
11. **Search, Filter & Pagination Utils** (`app/utils/pagination.py`)
12. **Automated Testing** (`tests/`)
13. **Docker & Deployment** (`Dockerfile`, `docker-compose.yml`)
