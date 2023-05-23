import json
from fastapi import WebSocket, WebSocketDisconnect
from string import ascii_uppercase
from random import choices
from ..stores.games import Game, games
import asyncio


def generate_pin(length: int) -> str:
    return "".join(choices(ascii_uppercase, k=length))


def generate_unique(length: int = 6) -> str:
    # this will loop continuously until a host disconnects if all 26**6 pins are taken
    while pin := generate_pin(length):
        if pin not in games:
            break
    return pin

async def restart_game(pin: str) -> None:
    if pin in games:
        game = games[pin]

        # Send a message to the host.
        await game.host.send_json({"type": "restart"})
        
        for vote in game.votes:
            game.votes[vote] = 0
        
        # Loop over the players in the game and send a message to each one
        for player in game.players:
            await player.socket.send_json({"type": "restart"})

async def host(websocket: WebSocket) -> None:
    pin = generate_unique()
    games[pin] = Game(websocket, [])

    await websocket.accept()
    await websocket.send_json({"type": "pin", "content": pin})

    # this disaster is convention; don't @ me
    try:
        while True:
            prompt = await websocket.receive_json()

            if prompt["type"] == "restart":
                await restart_game(pin)
            elif prompt["type"] == "prompt":
                tasks = (player.socket.send_json(prompt) for player in games[pin].players)
                await asyncio.gather(*tasks)

    except WebSocketDisconnect:
        del games[pin]
    