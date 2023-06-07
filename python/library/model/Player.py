from fastapi import WebSocket
from dataclasses import dataclass

@dataclass
class Player:
    pid: str
    socket: WebSocket
    name: str
    voted = False
