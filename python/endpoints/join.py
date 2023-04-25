from fastapi import WebSocket, WebSocketDisconnect
from .host import games


async def join(websocket: WebSocket, pin: str) -> None:
    await websocket.accept()

    if pin in games:
        game = games[pin]
        game.append(websocket)
        
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            games[pin].remove(websocket)
    else:
        # notify of a generic policy violation, since there's no proper equivalent to 404 for WebSockets
        await websocket.close(code=1008)
