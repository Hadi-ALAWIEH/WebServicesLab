from pydantic import BaseModel

class Course(BaseModel):
    id: int
    name: str
    instructor: str

class CourseCreate(BaseModel):
    name: str
    instructor: str
