import json
from fastapi import WebSocket, WebSocketDisconnect
from string import ascii_uppercase
from random import choices
from stores.games import Game, games
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
        await game.host.send_text(json.dumps({"action": "restart_game"}))
        
        # Loop over the players in the game and send a message to each one
        for player in game.players:
            await player.socket.send_text(json.dumps({"action": "restart_game"}))

async def host(websocket: WebSocket) -> None:
    pin = generate_unique()
    games[pin] = Game(websocket, [])

    await websocket.accept()
    await websocket.send_text(pin)

    # this disaster is convention; don't @ me
    try:
        while True:
            prompt = await websocket.receive_text()
            
            try:
                # Attempt to parse JSON string into Python dict (Object).
                parsed_prompt = json.loads(prompt)
                if parsed_prompt["action"] == "restart_game":
                    await restart_game(pin)
            except json.JSONDecodeError:
                print("Received an empty response or invalid JSON")
                tasks = (player.socket.send_text(prompt) for player in games[pin].players)
                await asyncio.gather(*tasks)
    except WebSocketDisconnect:
        del games[pin]
    