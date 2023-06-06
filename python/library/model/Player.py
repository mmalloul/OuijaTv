from fastapi import WebSocket
from dataclasses import dataclass
import uuid;

@dataclass
class Player:
    pid: uuid
    socket: WebSocket
    name: str
    voted = False
