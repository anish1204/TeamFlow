from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserOut, UserUpdate
from db import get_db
from utils.auth import get_current_user
from controllers import user as user_controller
from utils.auth import hash_password, verify_password, create_access_token, get_current_user_from_token
from pydantic import BaseModel

router = APIRouter()


class LoginData(BaseModel):
    username: str
    password: str


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if user_controller.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return user_controller.create_user(db, user)


@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    db_user = user_controller.get_user_by_username(db, data.username)
    if not db_user or not verify_password(data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

# Update a User


@router.patch("/user")
def update_user(data: UserUpdate, db: Session = Depends(get_db), curr_user=Depends(get_current_user)):
    
    new_user = curr_user
    new_user.name = data.name

    db.commit()
    db.refresh(new_user)

    return new_user


@router.delete("/user", status_code=204)
def delete_user(db: Session = Depends(get_db), curr_user=Depends(get_current_user)):
    db.delete(curr_user)
    db.commit()
    return

# @router.delete("/admin/{user_id}",status_code=204)
# def delete_user_by_admin(db:Session = Depends(get_db),)


@router.get("/me")
def read_current_user(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }
