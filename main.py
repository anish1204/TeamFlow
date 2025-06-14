from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
import models
from routes import auth, group,message
# from controllers.group import router as group_router

app = FastAPI()
bearer_scheme = HTTPBearer()
app.include_router(auth.router, prefix='/auth')
app.include_router(group.router, prefix='/group') 
app.include_router(message.router, prefix='/message')  