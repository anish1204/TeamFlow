from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import socketio
from routes import schedule

from routes import auth, group, message, ai

# Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

# FastAPI app
fastapi_app = FastAPI()

# CORS
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bearer_scheme = HTTPBearer()

# Routers
fastapi_app.include_router(auth.router, prefix='/auth')
fastapi_app.include_router(group.router, prefix='/group')
fastapi_app.include_router(message.router, prefix='/message')
fastapi_app.include_router(ai.router, prefix='/ai')
fastapi_app.include_router(schedule.router, prefix="/api")


# Mount FastAPI under Socket.IO
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)

# Import socket events
import sockets.events
