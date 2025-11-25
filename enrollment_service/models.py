from pydantic import BaseModel

class Enrollment(BaseModel):
    user_id: int
    course_id: int

class EnrollRequest(BaseModel):
    user_id: int
    course_id: int
