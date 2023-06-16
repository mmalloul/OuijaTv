from enum import Enum

# TODO: change to HostMessageType and PlayerMessageType?


class ClientMessageType(Enum):
    VOTE = "vote"
    RESTART = "restart"
    PROMPT = "prompt"
    WINNING_VOTE = "winningVote"

class ServerMessageType(Enum):
    PIN = "pin"
    JOINED = "joined"
    QUIT = "quit"
    PROMPT = "prompt"
    NO_VOTES = "noVotes"
    RESTART = "restart"
    ERROR = "error"
    VOTE = "vote"
    WINNING_VOTE = "winningVote"
    COUNTER = "counter"
    STOP_COUNTDOWN = "stopCountdown"
    WORD = "word"
    HOST_EXIT = "hostExit"
