from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.group import group_user_association, group_admin_association
from db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    role = Column(String, default="user")

    groups = relationship("Group", secondary=group_user_association, back_populates="users")
    admin_of_groups = relationship("Group", secondary=group_admin_association, back_populates="admin_list")
