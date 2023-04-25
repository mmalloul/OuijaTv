from fastapi import WebSocket, WebSocketDisconnect
from string import ascii_uppercase
from random import choices
from .stores.games import Game, games

def generate_pin(length: int) -> str:
    return "".join(choices(ascii_uppercase, k=length))


def generate_unique(length: int = 6) -> str:
    # this will loop continuously until a host disconnects if all 26**6 pins are taken
    while pin := generate_pin(length):
        if pin not in games:
            break
    return pin


async def host(websocket: WebSocket) -> None:
    pin = generate_unique()
    games[pin] = Game(websocket, [])

    await websocket.accept()
    await websocket.send_text(pin)

    # this disaster is convention; don't @ me
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_text(str(games))
    except WebSocketDisconnect:
        del games[pin]
