from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    date = Column(String)   # "2025-10-14"
    time = Column(String)   # "15:30"
    available = Column(Boolean, default=True)
    status = Column(String, default="PENDING")  # PENDING, ACCEPTED, DECLINED
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="notifications")
