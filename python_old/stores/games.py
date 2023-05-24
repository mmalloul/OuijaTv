from collections import defaultdict
from fastapi import WebSocket
from typing import Dict, List
from typing import NamedTuple
from string import ascii_uppercase, digits
from dataclasses import dataclass

options = [*(ascii_uppercase + digits), "GOODBYE"]

class Player(NamedTuple):
    name: str
    socket: WebSocket

@dataclass
class Game:
    host: WebSocket
    players: List[Player]
    votes: Dict[str, int]
    prompt: str = ""

    def __post_init__(self):
        self.votes = {option: 0 for option in options}

    def find_player_by_socket(self, socket: WebSocket) -> Player | None:
        for player in self.players:
            if player.socket == socket:
                return player
        return None

games: Dict[str, Game] = {}
