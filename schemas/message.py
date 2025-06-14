from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageCreate(BaseModel):
    content: str

class MessageOut(BaseModel):
    id: int
    content: str
    timestamp: datetime
    sender_id: int
    receiver_id: Optional[int]
    group_id: Optional[int]

    class Config:
        from_attributes = True
