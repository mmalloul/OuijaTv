from library.model.WebSocketClient import WebSocketClient

class Player:
    """
    A class representing a player in the game.
    ...
    """
    def __init__(self, name: str, room_token: str):
        self.name: str = name
        self.room_token: str = room_token
        self.websocket_client: WebSocketClient  = None