from enum import Enum


class ClientMessageType(Enum):
    VOTE = "vote"
    RESTART = "restart"
    PROMPT = "prompt"
    WINNING_VOTE = "winningVote"


class ServerMessageType(Enum):
    PIN = "pin"
    JOINED = "joined"
    PROMPT = "prompt"
    RESTART = "restart"
    ERROR = "error"
    VOTE = "vote"
    WINNING_VOTE = "winningVote"