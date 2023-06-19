from enum import Enum

# TODO: change to HostMessageType and PlayerMessageType?

class MessageType(Enum):
    RESTART = "restart"
    PROMPT = "prompt"
    QUIT = "quit"
    HOST_EXIT = "hostExit"
    WINNING_VOTE = "winningVote"
