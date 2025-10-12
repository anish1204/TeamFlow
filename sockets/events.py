from main import sio

@sio.event
async def connect(sid, environ):
    print(f"✅ Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"❌ Client disconnected: {sid}")

@sio.event
async def join_room(sid, data):
    room = data.get("room")
    if room:
        await sio.enter_room(sid, room)
        print(f"{sid} joined room {room}")

@sio.event
async def leave_room(sid, data):
    room = data.get("room")
    if room:
        await sio.leave_room(sid, room)
        print(f"{sid} left room {room}")

@sio.event
async def room_message(sid, data):
    room = data.get("room")
    message = data.get("message")
    sender = data.get("sender")
    if room and message and sender:
        print(f"📨 Message from {sender} to room {room}: {message}")
        await sio.emit("room_message", data, room=room)

@sio.event
async def join(sid, data):
    """data = { 'room': 'user_1' }"""
    room = data.get("room")
    if room:
        sio.enter_room(sid, room)
        print(f"✅ {sid} joined {room}")