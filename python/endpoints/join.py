from fastapi import WebSocket, WebSocketDisconnect
from ..stores.games import Player, Game, games


async def connect(websocket: WebSocket, game: Game, name: str) -> None:
    game.players.append(Player(name, websocket))
    await game.host.send_text(f"Player {name} joined")


async def disconnect(websocket: WebSocket, game: Game) -> None:
    player = game.find_player_by_socket(websocket)
    game.players.remove(player)
    await game.host.send_text(f"Player {player.name} left")


async def join(websocket: WebSocket, pin: str, name: str) -> None:
    await websocket.accept()

    if pin in games:
        await connect(websocket, games[pin], name)
        await websocket.send_text(f"You are here, {name}!")

        # terrible syntax, but a context manager would be too verbose
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            await disconnect(websocket, games[pin])
    else:
        # generic policy violation since there's no proper equivalent to 404
        await websocket.close(code=1008)
