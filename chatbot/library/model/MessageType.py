from enum import Enum

class MessageType(Enum):
    RESTART = "restart"
    PROMPT = "prompt"
    QUIT = "quit"
    HOST_EXIT = "hostExit"
    WINNING_VOTE = "winningVote"
