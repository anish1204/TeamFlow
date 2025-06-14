from sqlalchemy.orm import Session
from models.user import User
from fastapi import HTTPException
from schemas.user import UserCreate, UserOut
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create user 

def get_user_by_id(db:Session,user_id:int):
    db_user = db.query(User).filter(user_id == User.id).first()

    if not db_user:
        raise HTTPException(status_code=404,detail="User Not Found")
    
    return db_user


### Create a new user in the database
def create_user(db:Session , user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        name= user.name,
        email= user.email,
        username= user.username,
        password= hashed_password,
        role= user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

### Get a user by id from the database
def get_user(db:Session, user: int):
    return db.query(User).filter(User.id == user.id).first()

### Get a user by username from the database
def get_user_by_username(db:Session, username: str):
    return db.query(User).filter(User.username == username).first()

### Get a user by email from the database
def get_user_by_email(db:Session, email: str):
    return db.query(User).filter(User.email == email).first()

