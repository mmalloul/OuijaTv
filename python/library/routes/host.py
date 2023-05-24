from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from python.library.model.MessageType import ServerMessageType, ClientMessageType
from python.library.stores import games
from python.library.model import ServerMessage, ClientMessage


router = APIRouter()


@router.websocket("/host")
async def create_game(host: WebSocket):

    pin, game = games.new(host)

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
            prompt = await host.receive_json()
            prompt = ClientMessage.from_dictionary(prompt)

            match prompt.type:

                case ClientMessageType.RESTART:
                    await game.restart()
                
                case ClientMessageType.PROMPT:
                    await game.notify_host(
                        ServerMessage(
                            ServerMessageType.PROMPT, 
                            prompt.content,
                        ),
                    )

                case _:
                    await game.notify_host(
                        ServerMessage(
                            ServerMessageType.ERROR, 
                            "Invalid request",
                        ),
                    )
                    
                    
    except WebSocketDisconnect:
        games.remove(pin)