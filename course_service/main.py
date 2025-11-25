from fastapi import FastAPI, HTTPException
from models import Course, CourseCreate
from database import courses
import logging

app = FastAPI(title="Course Service")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("course-service")

@app.get("/courses")
def get_courses():
    return courses

@app.post("/courses")
def create_course(data: CourseCreate):
    new_id = len(courses) + 1
    course = Course(id=new_id, name=data.name, instructor=data.instructor)
    courses.append(course)
    logger.info(f"Course created: {course.name}")
    return course

@app.get("/courses/{course_id}")
def get_course(course_id: int):
    for c in courses:
        if c.id == course_id:
            return c
    raise HTTPException(status_code=404, detail="Course not found")
