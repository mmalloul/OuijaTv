from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from library.model.MessageType import ServerMessageType, ClientMessageType
from library.model import Player
from library.stores import games
from library.model import ServerMessage, ClientMessage


router = APIRouter()


@router.websocket("/join")
async def join_game(websocket: WebSocket, pin: str, username: str):

    await websocket.accept()

    if (game := games.items[pin]):

        player = Player(websocket, username)
        game.join(player)

        await game.notify_player(
            player,
            ServerMessage(
                ServerMessageType.PROMPT, 
                game.prompt,
            ),
        )

        # terrible syntax, but a context manager would be too verbose
        try:
            while True:
                message = await websocket.receive_json()
                message = ClientMessage.from_dictionary(message)

                if message.type == ClientMessageType.VOTE and (vote := message.content):
                    if vote in game.votes:
                        # might get overwhelming with many players
                        game.votes[vote] += 1

                        await game.notify_host(
                            ServerMessage(
                                ServerMessageType.VOTE, 
                                str(game.votes),
                            ),
                        )
                
        except WebSocketDisconnect:
            games.remove(pin, player)
    else:
        # generic policy violation since there's no proper equivalent to 404
        await websocket.close(code=1008)