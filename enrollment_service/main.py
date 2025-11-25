from fastapi import FastAPI, HTTPException
import requests
import logging

from models import EnrollRequest

app = FastAPI(title="Enrollment Service")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enrollment-service")

ENROLLMENTS = []

USER_SERVICE = "http://user-service:8001"
COURSE_SERVICE = "http://course-service:8002"

def check_user_exists(user_id):
    users = requests.get(f"{USER_SERVICE}/users").json()
    return any(u["id"] == user_id for u in users)

def check_course_exists(course_id):
    res = requests.get(f"{COURSE_SERVICE}/courses/{course_id}")
    return res.status_code == 200

@app.post("/enroll")
def enroll(data: EnrollRequest):
    if not check_user_exists(data.user_id):
        raise HTTPException(status_code=404, detail="User does not exist")

    if not check_course_exists(data.course_id):
        raise HTTPException(status_code=404, detail="Course does not exist")

    ENROLLMENTS.append({"user_id": data.user_id, "course_id": data.course_id})
    logger.info(f"User {data.user_id} enrolled in course {data.course_id}")

    return {"message": "Enrollment successful"}

@app.get("/students/{user_id}/courses")
def get_user_courses(user_id: int):
    user_courses = [
        e for e in ENROLLMENTS if e["user_id"] == user_id
    ]
    return user_courses
