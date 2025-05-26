from db import engine
from models import user  # make sure this imports your User model

user.Base.metadata.create_all(bind=engine)
