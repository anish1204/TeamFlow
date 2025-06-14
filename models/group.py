from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

group_user_association = Table(
    "group_user_association",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("groups.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)

group_admin_association = Table(
    "group_admin_association",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("groups.id")),
    Column("admin_id", Integer, ForeignKey("users.id"))
)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", secondary=group_user_association, back_populates="groups")
    admin_list = relationship("User", secondary=group_admin_association, back_populates="admin_of_groups")
