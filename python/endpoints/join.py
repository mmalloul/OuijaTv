from fastapi import WebSocket, WebSocketDisconnect
from ..stores.games import Player, Game, games


async def connect(websocket: WebSocket, game: Game, name: str) -> None:
    game.players.append(Player(name, websocket))
    await game.host.send_json({"type": "connect", "username": name})


async def disconnect(websocket: WebSocket, game: Game) -> None:
    if (player := game.find_player_by_socket(websocket)):
        game.players.remove(player)
        await game.host.send_json({"type": "disconnect", "username": player.name})


async def join(websocket: WebSocket, pin: str, name: str) -> None:
    await websocket.accept()

    if pin in games:
        await connect(websocket, games[pin], name)

        # terrible syntax, but a context manager would be too verbose
        try:
            while True:
                message = await websocket.receive_json()

                if message["type"] == "vote" and (vote := message["content"]):
                    if vote in games[pin].votes:
                        # might get overwhelming with many players
                        games[pin].votes[vote] += 1
                        await games[pin].host.send_json({"type": "votes", "content": games[pin].votes})
                
        except WebSocketDisconnect:
            await disconnect(websocket, games[pin])
    else:
        # generic policy violation since there's no proper equivalent to 404
        await websocket.close(code=1008)
