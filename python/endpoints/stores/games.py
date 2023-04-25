from fastapi import WebSocket
from typing import Dict, List
from typing import NamedTuple

class Game(NamedTuple):
    host: WebSocket
    players: List[WebSocket]

games: Dict[str, Game] = {}
