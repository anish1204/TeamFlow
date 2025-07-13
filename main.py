from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware  # 👈 CORS middleware
from typing import List, Optional
import models
from routes import auth, group, message,ai

app = FastAPI()

# 👇 Add CORS Middleware here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bearer_scheme = HTTPBearer()

# Include your routers
app.include_router(auth.router, prefix='/auth')
app.include_router(group.router, prefix='/group') 
app.include_router(message.router, prefix='/message')  
app.include_router(ai.router, prefix="/ai")
