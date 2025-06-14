from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import group
from models.message import Message
from models.user import User
from schemas.message import MessageCreate, MessageOut
from db import get_db
from utils.auth import get_current_user
from typing import List

router = APIRouter(prefix="", tags=["Messages"])

# Send Message to a user
@router.post("/user/{receiver_id}")
def send_private_msg(
receiver_id:int,
msg_data:MessageCreate,
db : Session = Depends(get_db),
sender : User = Depends(get_current_user)
):
    sender_id = sender.id
    content = msg_data.content
    msg = Message(
        content=content,
        sender_id=sender_id,
        receiver_id = receiver_id,
    )
    db.add(msg)
    db.commit()
    return msg


@router.patch("/message/{message_id}")
def update_msg(
    message_id:int,
    msg_data:MessageCreate,
    db : Session = Depends(get_db),
    curr_user : User = Depends(get_current_user)
):
    
    curr_msg = db.query(Message).filter(Message.id == message_id).first()
    if curr_msg.sender_id != curr_user.id:
        raise HTTPException(status_code=403,detail="Not Authorized to Edit")
    else:
     curr_msg.content = msg_data.content
     db.commit() 
     return "Edited Successfully"
    

###Send all groups to a user





# 1. Send private message to a user
# @router.post("/user/{receiver_id}")
# def send_private_message(
#     receiver_id: int,
#     msg_data: MessageCreate,
#     db: Session = Depends(get_db),
#     sender: User = Depends(get_current_user)
# ):
#     receiver = db.query(User).filter(User.id == receiver_id).first()
#     if not receiver:
#         raise HTTPException(status_code=404, detail="Receiver not found")

#     msg = message(
#         content=msg_data.content,
#         sender_id=sender.id,
#         receiver_id=receiver.id
#     )
#     db.add(msg)
#     db.commit()
#     db.refresh(msg)
#     return {"message": f"Sent to {receiver.username}", "id": msg.id}


# # 2. Send group message (to all users + admins except sender)
# @router.post("/group/{group_id}")
# def send_group_message(
#     group_id: int,
#     msg_data: MessageCreate,
#     db: Session = Depends(get_db),
#     sender: user = Depends(get_current_user)
# ):
#     group = db.query(group).filter(group.id == group_id).first()
#     if not group:
#         raise HTTPException(status_code=404, detail="Group not found")

#     if sender not in group.users and sender not in group.admin_list:
#         raise HTTPException(status_code=403, detail="You are not in the group")

#     recipients = list(set(group.users + group.admin_list))
#     recipients = [u for u in recipients if u.id != sender.id]

#     for user in recipients:
#         msg = message(
#             content=msg_data.content,
#             sender_id=sender.id,
#             receiver_id=user.id,
#             group_id=group.id
#         )
#         db.add(msg)

#     db.commit()
#     return {"message": f"Message sent to {len(recipients)} users in group '{group.name}'"}


# 3. Get all messages for current user
@router.get("/me", response_model=List[MessageOut])
def get_my_messages(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    messages = db.query(Message).filter(Message.receiver_id == user.id).order_by(Message.timestamp.desc()).all()
    return messages


# # 4. Get all messages sent to a group
# @router.get("/group/{group_id}", response_model=List[MessageOut])
# def get_group_messages(
#     group_id: int,
#     db: Session = Depends(get_db),
#     user: user = Depends(get_current_user)
# ):
#     group = db.query(group).filter(group.id == group_id).first()
#     if not group:
#         raise HTTPException(status_code=404, detail="Group not found")

#     if user not in group.users and user not in group.admin_list:
#         raise HTTPException(status_code=403, detail="Not a group member")

#     messages = db.query(message).filter(message.group_id == group.id).order_by(message.timestamp.desc()).all()
#     return messages
