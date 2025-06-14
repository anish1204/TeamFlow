from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.orm import Session
from models.group import Group
from models.user import User
from schemas.group import GroupCreate, GroupUpdate, GroupResponse ,GroupDetailResponse
from db import get_db
from utils.auth import get_current_user

router = APIRouter()


@router.post("/create")
def create_group(
    group_data:GroupCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_user)
):
    if not admin_user:
        raise HTTPException(status_code=404,detail="Admin Not found")

    existing_group = db.query(Group).filter(Group.name == group_data.name).first()
    if existing_group:
        raise HTTPException(status_code=400, detail="Group with similar name exists")

    new_group = Group(name=group_data.name)
    
    # Assuming Group has admin_list and users_id as relationship fields
    # new_group.admin_list.append(admin_user)
    new_group.users.append(admin_user)
    new_group.admin_list.append(admin_user)
    
    db.add(new_group)
    db.commit()


    return new_group; 

### Get all Groups
@router.get("/getgroups")
def get_all_groups(
    db:Session = Depends(get_db),

):
    all_groups = db.query(Group).all()
    return all_groups

### Get Specific Groups
@router.get("/get/{group_id}", response_model=GroupDetailResponse)
def get_specific_group(
    group_id: int,
    db: Session = Depends(get_db),
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return {
        "id": group.id,
        "name": group.name,
        "user_ids": [user.id for user in group.users],
        "admin_ids": [admin.id for admin in group.admin_list],
    }



### Add a User to a Group
@router.post("/add/{group_id}/{user_id}")
def add_user_to_group(
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user in group.users:
        raise HTTPException(status_code=400, detail="User already in group")

    group.users.append(user)
    db.commit()
    db.refresh(group)

    return group

# Delete the user 
@router.delete("/delete/{group_id}")
def delete_group(
    group_id: int,
    db:Session = Depends(get_db),
    curr_user = Depends(get_current_user),
    
):
    group = db.query(Group).get(group_id)
    return group
























































# @router.post("/create", response_model=GroupResponse)
# def create_group(
#     group_data: GroupCreate,
#     db: Session = Depends(get_db),
#     admin_user: User = Depends(get_current_user)
# ):
#     if not admin_user:
#         raise HTTPException(status_code=404, detail="No such user exists")

#     existing_group = db.query(Group).filter(Group.name == group_data.name).first()
#     if existing_group:
#         raise HTTPException(status_code=400, detail="Group already exists")

#     group = Group(name=group_data.name)
#     group.users.append(admin_user)

#     db.add(group)
#     db.commit()
#     db.refresh(group)
#     return group


# @router.put("/update/{group_id}", response_model=GroupResponse)
# def update_group(
#     group_id: int,
#     data: GroupUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     group = db.query(Group).get(group_id)
#     if not group:
#         raise HTTPException(status_code=404, detail="Group not found")

#     if data.name:
#         group.name = data.name

#     db.commit()
#     db.refresh(group)
#     return group


# @router.delete("/delete/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_group(
#     group_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     group = db.query(Group).get(group_id)
#     if not group:
#         raise HTTPException(status_code=404, detail="Group not found")

#     db.delete(group)
#     db.commit()
#     return {"message": "Group deleted successfully"}


# @router.get("/all", response_model=list[GroupResponse])
# def get_all_groups(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return db.query(Group).all()


# @router.post("/add-user")
# def add_user_to_group(
#     user_id: int,
#     group_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     group = db.query(Group).get(group_id)
#     user = db.query(User).get(user_id)

#     if not group or not user:
#         raise HTTPException(status_code=404, detail="Group or User not found")

#     if user in group.users:
#         raise HTTPException(status_code=400, detail="User already in group")

#     group.users.append(user)
#     db.commit()
#     return {"message": f"User {user_id} added to group {group_id}"}
