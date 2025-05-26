from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import models
from routes import auth

app = FastAPI()
app.include_router(auth.router, prefix='/auth')