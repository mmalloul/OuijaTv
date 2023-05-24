from enum import Enum


class ClientMessageType(Enum):
    VOTE = "vote"
    RESTART = "restart"
    PROMPT = "prompt"


class ServerMessageType(Enum):
    PIN = "pin"
    PROMPT = "prompt"
    RESTART = "restart"
    ERROR = "error"
    VOTE = "vote"