from fastapi import FastAPI

app = FastAPI(
    title="Student Management System",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Student Management System API"
    }