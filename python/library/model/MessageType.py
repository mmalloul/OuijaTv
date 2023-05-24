from enum import Enum


class MessageType(Enum):
    pass


class ClientMessageType(MessageType):
    VOTE = 0


class ServerMessageType(MessageType):
    PROMPT = 0
    RESTART = 1