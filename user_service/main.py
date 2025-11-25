from fastapi import FastAPI, HTTPException
from models import User, RegisterRequest, LoginRequest
from database import users
import logging

app = FastAPI(title="User Service")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("user-service")

@app.post("/register")
def register_user(data: RegisterRequest):
    user_id = len(users) + 1
    user = User(id=user_id, username=data.username, password=data.password)
    users.append(user)
    logger.info(f"User registered: {user.username}")
    return {"message": "User registered", "user_id": user_id}

@app.post("/login")
def login(data: LoginRequest):
    for u in users:
        if u.username == data.username and u.password == data.password:
            logger.info(f"User logged in: {u.username}")
            return {"message": "Login successful", "user_id": u.id}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/users")
def list_users():
    return users
