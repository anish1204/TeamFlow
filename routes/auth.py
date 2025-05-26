from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserOut
from db import get_db
from controllers import user as user_controller
from utils.auth import hash_password, verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter()

class LoginData(BaseModel):
    username: str
    password: str

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate,db : Session = Depends(get_db)):
    if user_controller.get_user_by_email(db,user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return user_controller.create_user(db, user)

@router.post("/login")
def login(data:LoginData,db:Session = Depends(get_db)):
    db_user = user_controller.get_user_by_username(db,data.username)
    if not db_user or not verify_password(data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}