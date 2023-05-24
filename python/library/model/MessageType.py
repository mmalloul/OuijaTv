from enum import Enum


class MessageType(Enum):
    pass


class ClientMessageType(MessageType):
    VOTE = "vote"
    RESTART = "restart"
    PROMPT = "prompt"


class ServerMessageType(MessageType):
    PIN = "pin"
    PROMPT = "prompt"
    RESTART = "restart"
    ERROR = "error"