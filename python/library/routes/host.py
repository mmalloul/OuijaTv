from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from library.model.MessageType import ServerMessageType, ClientMessageType
from library.stores import games
from library.model import ServerMessage, ClientMessage


router = APIRouter()


@router.websocket("/host")
async def create_game(host: WebSocket, name: str, voting_time: str, game_mode: str):

    pin, game = games.new(host, name, int(voting_time), game_mode)

    await host.accept()
    await game.notify_host(
        ServerMessage(
            ServerMessageType.PIN, 
            pin,
        ),
    )

    # this disaster is convention; don't @ me
    try:
        while True:
            message = await host.receive_json()
            message = ClientMessage.from_dictionary(message)
            match message.type:
                case ClientMessageType.WINNING_VOTE:
                    await game.broadcast(
                        ServerMessage(
                            ServerMessageType.WINNING_VOTE,
                            message.content
                        )
                    )
                case ClientMessageType.RESTART:
                    await game.restart()
                
                case ClientMessageType.PROMPT:
                    await game.broadcast(
                        ServerMessage(
                            ServerMessageType.PROMPT, 
                            message.content,
                        ),
                    )
                    game.start_countdown()


                case _:
                    await game.notify_host(
                        ServerMessage(
                            ServerMessageType.ERROR, 
                            "Invalid request type",
                        ),
                    )
                    
                    
    except WebSocketDisconnect:
        games.remove(pin)