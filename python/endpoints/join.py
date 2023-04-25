from fastapi import WebSocket, WebSocketDisconnect
from stores.games import Game, games


async def connect(websocket: WebSocket, game: Game) -> None:
    game.players.append(websocket)
    number = len(game.players)
    await game.host.send_text(f"Player {number} joined")


async def disconnect(websocket: WebSocket, game: Game) -> None:
    number = len(game.players)
    game.players.remove(websocket)
    await game.host.send_text(f"Player {number} left")


async def join(websocket: WebSocket, pin: str) -> None:
    await websocket.accept()

    if pin in games:
        await connect(websocket, games[pin])
        await websocket.send_text("You are here!")

        # terrible syntax, but a context manager would be too verbose
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            await disconnect(websocket, games[pin])
    else:
        # generic policy violation since there's no proper equivalent to 404
        await websocket.close(code=1008)
