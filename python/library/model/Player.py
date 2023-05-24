from fastapi import WebSocket
from typing import NamedTuple


class Player(NamedTuple):
    socket: WebSocket
    name: str
