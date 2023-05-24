from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from python.library.model.MessageType import ServerMessageType, ClientMessageType
from python.library.stores import games
from python.library.model import Message


router = APIRouter()


@router.websocket("/host")
async def create_game(host: WebSocket):

    pin, game = games.new(host)

    await host.accept()
    await game.notify_host(
        Message[ServerMessageType](
            ServerMessageType.PIN, 
            pin,
        ),
    )

    # this disaster is convention; don't @ me
    try:
        while True:
            prompt: Message[ClientMessageType] = await host.receive_json()

            match prompt.type:

                case ClientMessageType.RESTART:
                    await game.restart()
                
                case ClientMessageType.PROMPT:
                    await game.notify_host(
                        Message[ServerMessageType](
                            ServerMessageType.PROMPT, 
                            prompt.content,
                        ),
                    )

                case _:
                    await game.notify_host(
                        Message[ServerMessageType](
                            ServerMessageType.ERROR, 
                            "Invalid request",
                        ),
                    )
                    
                    
    except WebSocketDisconnect:
        games.remove(pin)