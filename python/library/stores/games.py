from fastapi import WebSocket
from string import ascii_uppercase
from random import choices
from library.model import Game, Player
from library.model import Game
from dotenv import load_dotenv
import os
import requests

# Load variables from .env file
load_dotenv('../../.env')

# use this module as a singleton

items: dict[str, Game] = {}


def _generate_pin(length: int) -> str:
    return "".join(choices(ascii_uppercase, k=length))


def new(host: WebSocket, gameName: str, voting_time: str, game_mode: str, twitch_channel: str, length: int = 6) -> tuple[str, Game]:

    # this will loop continuously until a host disconnects if all 26**6 pins are taken
    while pin := _generate_pin(length):
        if pin not in items:
            break
    
    game = Game(host, name=gameName, voting_time=voting_time, game_mode=game_mode, twitch_channel=twitch_channel)
    items[pin] = game

    return pin, game


def remove(pin: str, player: Player | None = None) -> None:
    if pin not in items: 
        return
        
    if player:
        items[pin].players.remove(player)
    else:
        stop_twitch_bot(pin)
        del items[pin]

def stop_twitch_bot(pin):
    base_url = os.getenv('PUBLIC_TWITCH_URL')
    url = f'{base_url}/twitch/stop?room_token={pin}'
    try:
        requests.post(url)
        print(f"Requesting chatbot server to kill bot in room: {pin}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
   
