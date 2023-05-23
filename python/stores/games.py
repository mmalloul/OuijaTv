from fastapi import WebSocket
from typing import Dict, List
from typing import NamedTuple

class Player(NamedTuple):
    name: str
    socket: WebSocket

class Game(NamedTuple):
    host: WebSocket
    players: List[Player]

    def findPlayerBySocket(self, socket: WebSocket) -> Player:
        for player in self.players:
            if player.socket == socket:
                return player
        return None

games: Dict[str, Game] = {}
