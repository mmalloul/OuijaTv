from fastapi import WebSocket
from string import ascii_uppercase
from random import choice

pin_length = 6

async def host(websocket: WebSocket):
    
    pin = "".join(choice(ascii_uppercase) for _ in range(pin_length))
    
    await websocket.accept()
    await websocket.send_text(pin)
    await websocket.close()