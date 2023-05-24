from fastapi import WebSocket
from python.library.model import Game, Player
from string import ascii_uppercase
from random import choices
from python.library.model import Game

# use this module as a singleton

items: dict[str, Game] = {}


def _generate_pin(length: int) -> str:
    return "".join(choices(ascii_uppercase, k=length))


def new(host: WebSocket, length: int = 6) -> tuple[str, Game]:

    # this will loop continuously until a host disconnects if all 26**6 pins are taken
    while pin := _generate_pin(length):
        if pin not in items:
            break
    
    game = Game(host)
    items[pin] = game

    return pin, game


def remove(pin: str, player: Player | None = None) -> None:

    if player:
        items[pin].players.remove(player)
    else:
        del items[pin]