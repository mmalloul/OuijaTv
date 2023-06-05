from enum import Enum

# TODO: change to HostMessageType and PlayerMessageType?


class ClientMessageType(Enum):
    VOTE = "vote"
    RESTART = "restart"
    PROMPT = "prompt"


class ServerMessageType(Enum):
    PIN = "pin"
    JOINED = "joined"
    PROMPT = "prompt"
    RESTART = "restart"
    ERROR = "error"
    VOTE = "vote"
    COUNTER = "counter"
    WORD = "word"