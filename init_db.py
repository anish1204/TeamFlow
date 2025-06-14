from db import Base,engine
from models import user, message, group

Base.metadata.drop_all(bind=engine)


user.Base.metadata.create_all(bind=engine)
message.Base.metadata.create_all(bind=engine)
group.Base.metadata.create_all(bind=engine)
