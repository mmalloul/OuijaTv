from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from library.model.MessageType import ServerMessageType, ClientMessageType
from library.model import Player
from library.stores import games
from library.model import ServerMessage, ClientMessage
import uuid

router = APIRouter()


@router.websocket("/join")
async def join_game(websocket: WebSocket, pin: str, username: str):
    await websocket.accept()

    if game := games.items[pin]:
        player = Player(str(uuid.uuid4()), websocket, username)
        game.join(player)

        await game.broadcast(
            ServerMessage(
                ServerMessageType.JOINED,
                {"pid": player.pid, "name": player.name},
            )
        )

        await game.notify_player(
            player,
            ServerMessage(
                ServerMessageType.PROMPT, 
                game.prompt
            ),
        )

        await game.notify_player(
            player,
            ServerMessage(
                ServerMessageType.WORD,
                game.word
            )
        )
        
        await game.notify_player(
            player,
            ServerMessage(
                ServerMessageType.WINNING_VOTE,
                game.winning_letter
            )
        )
        # terrible syntax, but a context manager would be too verbose
        try:
            while True:
                message = await websocket.receive_json()
                message = ClientMessage.from_dictionary(message)

                match message.type:
                    case ClientMessageType.VOTE:
                        if (vote := message.content) and vote in game.votes:
                            # might get overwhelming with many players
                            await game.vote(vote, player)

                    case _:
                        await game.notify_player(
                            player,
                            ServerMessage(
                                ServerMessageType.ERROR,
                                "Invalid request type",
                            ),
                        )

        except WebSocketDisconnect:
            games.remove(pin, player)
            await game.broadcast(ServerMessage(ServerMessageType.QUIT, player.pid))
    else:
        # generic policy violation since there's no proper equivalent to 404
        await websocket.close(code=1008)
