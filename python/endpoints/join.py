from fastapi import WebSocket, WebSocketDisconnect
from .host import Game, games


async def join(websocket: WebSocket, pin: str) -> None:
    await websocket.accept()

    if pin in games:
        game = games[pin]
        game.players.append(websocket)
        name = f"Player {len(game.players)}"
        
        await game.host.send_text(f"{name} joined")
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            games[pin].players.remove(websocket)
            await game.host.send_text(f"{name} left")
    else:
        # notify of a generic policy violation, since there's no proper equivalent to 404 for WebSockets
        await websocket.close(code=1008)
