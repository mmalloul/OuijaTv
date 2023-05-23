from fastapi import WebSocket
from typing import Dict, List
from typing import NamedTuple
from string import ascii_uppercase, digits

options = [*(ascii_uppercase + digits), "GOODBYE"]

class Player(NamedTuple):
    name: str
    socket: WebSocket

class Game(NamedTuple):
    host: WebSocket
    players: List[Player]
    votes: Dict[str, int] = {option: 0 for option in options}

    def find_player_by_socket(self, socket: WebSocket) -> Player | None:
        for player in self.players:
            if player.socket == socket:
                return player
        return None

games: Dict[str, Game] = {}
