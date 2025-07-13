# models/friendship.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from db import Base

friend_association = Table(
    'friend_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('friend_id', Integer, ForeignKey('users.id'))
)
