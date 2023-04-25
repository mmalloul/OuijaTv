from fastapi import WebSocket, WebSocketDisconnect
from string import ascii_uppercase
from random import choice

games = {}


def generate_pin(length: int) -> str:
    return "".join(choice(ascii_uppercase) for _ in range(length))


def generate_unique(length: int = 6) -> str:
    # this will loop until a host disconnects if all 26**6 pins are taken
    while pin := generate_pin(length):
        if pin not in games:
            break
    return pin


def generate_unique(length: int = 6) -> str:
    pin = generate_pin(length)
    if pin not in games:
        return pin
    else:
        return generate_unique(length)


async def host(websocket: WebSocket):
    
    pin = generate_unique()
    games[pin] = websocket

    await websocket.accept()
    await websocket.send_text(pin)

    # this disaster is convention; don't @ me
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        del games[pin]
