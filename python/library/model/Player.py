from fastapi import WebSocket
from dataclasses import dataclass


@dataclass
class Player:
    socket: WebSocket
    name: str
    voted = False
