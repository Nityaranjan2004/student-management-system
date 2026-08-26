# 🎓 Student Management System — Quick Schema Reference

---

## 🗺️ 1. Visual Flow & Connections

```
┌────────────────────────────────────────────────────────┐
│                      USERS (Table)                     │
├──────────────────────────────────────┬─────────────────┤
│ id                                   │ [PK] ──────────┐│
│ email, username                      │ [UK]           ││
│ hashed_password, first_name, ...     │                ││
└──────────────────────────────────────┴────────────────┼┘
                                                        │
                        ┌───────────────────────────────┴───────────────────────────────┐
                        │ (1-to-1)                                                      │ (1-to-1)
                        ▼                                                               ▼
┌──────────────────────────────────────┐                       ┌──────────────────────────────────────┐
│           STUDENTS (Table)           │                       │           TEACHERS (Table)           │
├──────────────────────────────────────┤                       ├──────────────────────────────────────┤
│ id                        [PK] ─────┐│                       │ id                        [PK] ─────┐│
│ user_id                   [FK] ──> U ││                       │ user_id                   [FK] ──> U ││
│ roll_number               [UK]      ││                       │ employee_id               [UK]      ││
│ dob, gender, grade, ...             ││                       │ department, phone, ...              ││
└─────────────────────────────────────┼┘                       └─────────────────────────────────────┼┘
                                      │                                                              │ (1-to-Many)
                                      │                                                              ▼
                                      │                        ┌──────────────────────────────────────┐
                                      │                        │           COURSES (Table)            │
                                      │                        ├──────────────────────────────────────┤
                                      │                        │ id                        [PK] ─────┐│
                                      │                        │ code                      [UK]      ││
                                      │                        │ title, credits, ...                 ││
                                      │                        │ teacher_id                [FK] ──> T││
                                      │                        └─────────────────────────────────────┼┘
                                      │                                                              │
                                      └───────────────────────────────┬──────────────────────────────┘
                                         (1-to-Many)                  │ (1-to-Many)
                                         students.id                  │ courses.id
                                                                      ▼
                                      ┌───────────────────────────────────────────────────────────────┐
                                      │                      ENROLLMENTS (Table)                      │
                                      ├───────────────────────────────────────────────────────────────┤
                                      │ id          [PK]                                              │
                                      │ student_id  [FK] ──> students.id                              │
                                      │ course_id   [FK] ──> courses.id                               │
                                      │ status, grade, enrolled_at                                    │
                                      └───────────────────────────────────────────────────────────────┘
```

---

## 📋 2. Compact All-In-One Table

| Table | Column Name | Key | References | Description |
| :--- | :--- | :---: | :--- | :--- |
| **`users`** | `id` | **`[PK]`** | — | Unique user ID |
| | `email` | **`[UK]`** | — | Login email |
| | `username` | **`[UK]`** | — | Username |
| | `hashed_password` | — | — | Password hash |
| | `first_name`, `last_name` | — | — | Full name |
| | `role` | — | — | `admin` \| `teacher` \| `student` |
| | `is_active` | — | — | Active status |
| | `created_at`, `updated_at` | — | — | Timestamps |
| **`students`** | `id` | **`[PK]`** | — | Unique student ID |
| | `user_id` | **`[FK]`** | 🔗 **`users.id`** | 1-to-1 account link (`CASCADE`) |
| | `roll_number` | **`[UK]`** | — | Unique roll number |
| | `date_of_birth`, `gender` | — | — | Demographics |
| | `grade_level`, `section` | — | — | Class details |
| | `guardian_name`, `phone`, `email` | — | — | Guardian info |
| | `address` | — | — | Residential address |
| **`teachers`** | `id` | **`[PK]`** | — | Unique teacher ID |
| | `user_id` | **`[FK]`** | 🔗 **`users.id`** | 1-to-1 account link (`CASCADE`) |
| | `employee_id` | **`[UK]`** | — | Unique employee ID |
| | `department` | — | — | e.g. Computer Science |
| | `qualification`, `specialization` | — | — | Degrees & subject |
| | `phone`, `hire_date` | — | — | Contact & join date |
| **`courses`** | `id` | **`[PK]`** | — | Unique course ID |
| | `code` | **`[UK]`** | — | Course code (e.g. `CS101`) |
| | `title`, `description` | — | — | Course information |
| | `credits`, `semester` | — | — | Credit hours & term |
| | `is_active` | — | — | Active status |
| | `teacher_id` | **`[FK]`** | 🔗 **`teachers.id`** | Assigned teacher (`SET NULL`) |
| **`enrollments`** | `id` | **`[PK]`** | — | Unique enrollment ID |
| | `student_id` | **`[FK]`** | 🔗 **`students.id`** | Enrolled student (`CASCADE`) |
| | `course_id` | **`[FK]`** | 🔗 **`courses.id`** | Target course (`CASCADE`) |
| | `status` | — | — | `enrolled` \| `completed` \| `dropped` |
| | `grade` | — | — | Grade (e.g. `A`, `92`) |
| | `enrolled_at` | — | — | Enrollment date |
