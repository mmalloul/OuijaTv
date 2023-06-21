from typing import List, Optional
from library.model.Player import Player
from library.model.MessageType import MessageType
from library.model.WebSocketClient import WebSocketClient

import json
import os

from dotenv import load_dotenv
load_dotenv('../.env')

class Game:
    """
    A class representing a game.
    """
    def __init__(self, channel_name: str, room_token: str):
        """
        Initializes a Game instance.

        Parameters:
        - channel_name (str): The name of the game channel.
        - room_token (str): The token for the game room.
        """
        self.room_token = room_token
        self.channel_name = channel_name
        self.active_players: List[Player] = []

    async def connect_player_to_game(self, player: Player):
        """
        Adds a player to the game by establishing a websocket connection through the WebSocketClient class.

        Parameters:
        - player (Player): The player to be added.

        Raises:
        - Exception: If an error occurs during the connection process.
        """
        try:
            url: str = f"{os.getenv('PUBLIC_WS_URL')}/join?pin={self.room_token}&username={player.name}"
            websocket_client: WebSocketClient = WebSocketClient(url)
            player.websocket_client = websocket_client

            await player.websocket_client.connect()

            self.add_player_to_active_player_list(player)
            print(f"Player {player.name} added to the game.")

            message = await player.websocket_client.receive_messages()
            message = json.loads(message)

            print(message)

            if message["type"] == MessageType.QUIT.value:
                self.remove_player_from_active_players_list(self)
                
                player.websocket.close()
                print("Connection closed by the server.")
        except Exception as e:
            print(f"Error occurred: {str(e)}")

    async def player_votes(self, player: Player, vote: str):
        """
        Sends a vote from a player.

        Parameters:
        - player (Player): The player who is sending the vote.
        - vote (str): The vote content.
        ...
        """
        if player.websocket_client:
            print(f"sending vote: {vote}")

            message = json.dumps({
                "type": "vote",
                "content": vote,
            })
            await player.websocket_client.send_message(message)

    def is_player_new(self, player: Player):
        """
        Checks if a player is new.

        Parameters:
        - player (Player): The player to check.

        Returns:
        - bool: True if the player is new, False otherwise.
        """
        return not any(active_player.name == player.name for active_player in self.active_players)

    def add_player_to_active_player_list(self, player: Player):
        """
        Adds a player to the active players list.

        Parameters:
        - player (Player): The player to add.
        """
        self.active_players.append(player)

    def remove_player_from_active_players_list(self, player: Player):
        """
        Removes a player from the active players list.

        Parameters:
        - player (Player): The player to remove.
        """
        if player in self.active_players:
            self.active_players.remove(player)

    def get_player_by_name(self, player_name: str) -> Optional[Player]:
        """
        Gets a player by their name.

        Parameters:
        - player_name (str): The name of the player to get.

        Returns:
        - Optional[Player]: The player object if found, None otherwise.
        """
        return next((player for player in self.active_players if player.name == player_name), None)
