from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str
