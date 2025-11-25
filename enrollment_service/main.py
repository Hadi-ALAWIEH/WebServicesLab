from fastapi import FastAPI, HTTPException
import requests
import logging
import redis
import json

from models import EnrollRequest

app = FastAPI(title="Enrollment Service")
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enrollment-service")

ENROLLMENTS = []

USER_SERVICE = "http://user-service:8001"
COURSE_SERVICE = "http://course-service:8002"

def check_user_exists(user_id):
    cache_key = f"user:{user_id}"

    # 1) Check Redis cache first
    cached = redis_client.get(cache_key)
    if cached:
        return True  # we don't store False

    # 2) If not cached → call User Service
    users = requests.get(f"{USER_SERVICE}/users").json()
    exists = any(u["id"] == user_id for u in users)

    # 3) Store only positive results in cache (avoid caching misses)
    if exists:
        redis_client.set(cache_key, "1", ex=60)  # expire in 60 seconds

    return exists

def check_course_exists(course_id):
    cache_key = f"course:{course_id}"

    # Check Redis first
    cached = redis_client.get(cache_key)
    if cached:
        return True

    res = requests.get(f"{COURSE_SERVICE}/courses/{course_id}")

    if res.status_code == 200:
        redis_client.set(cache_key, "1", ex=60)
        return True

    return False

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
