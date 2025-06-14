from pydantic import BaseModel
from typing import List, Optional
from schemas.user import UserBasicResponse

class GroupCreate(BaseModel):
    name: str
    users_id:Optional[List[int]] = []
    # admin_list:Optional[List[Users]] = []

class GroupUpdate(BaseModel):
    name : Optional[str] = None

class GroupResponse(BaseModel):
    id: int
    name: str
    users_id: List[UserBasicResponse]
    # admin_list:Optional[List[int]]
    class Config:
        from_attributes = True

class GroupDetailResponse(BaseModel):
    id: int
    name: str
    user_ids: List[int]
    admin_ids: List[int]

    class Config:
        orm_mode = True
