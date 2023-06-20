from twitchio.ext import commands
from library.model.Player import Player
from library.model.Game import Game
from string import ascii_uppercase, digits
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv('../.env')

class Bot(commands.Bot):
    """
    A Twitch bot class for handling game commands and messages.
    """

    client_id: str = os.getenv("TWITCH_CLIENT_ID")
    token: str = os.getenv("TWITCH_TOKEN")
    play: str = "PLAY"
    goodbye: str = "GOODBYE"
    prefix: str = "!"

    def __init__(self, channel_name: str, game: Game):
        """
        Initialize the Bot object.

        Parameters:
        - channel_name: The name of the Twitch channel.
        - game: The game object associated with the bot.
        """
        super().__init__(token=self.token, prefix="!", initial_channels=[channel_name])
        self.game = game

    async def event_ready(self):
        """
        Event handler for when the bot is ready.
        """
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    async def event_message(self, message):
        """
        Event handler for incoming chat messages.

        Parameters:
        - message: The incoming chat message object.
        """
        if message.author.name.lower() != self.nick.lower():
            name = message.author.name

            # Remove leading and trailing whitespace and convert to uppercase
            message_content = message.content.strip().upper()

            # Check if the message starts with an exclamation mark
            if message_content.startswith(self.prefix):
                message_content = message_content[1:]  # Remove the exclamation mark

                print(f"New message from {name}: {message_content}")

                # Check if the player is already in the game, if not it will create a new player
                player: Player = self.game.get_player_by_name(name) or Player(name, self.game)

                if message_content == self.play:
                    await self.game.connect_player_to_game(player)
                else:
                    await self.process_vote(player, message_content)

    async def process_vote(self, player: Player, vote: str):
        """
        Process a vote message.

        Parameters:
        - player: The Player object associated with the vote.
        - vote: The vote value.

        Checks if the vote is valid and passes it to the game object.
        Vote must be a single alphabetic, numeric character, or 'GOODBYE'.
        """
        if (vote in ascii_uppercase or vote in digits) or vote == self.goodbye:
            if vote == self.goodbye:
                vote = "!"
            await self.game.player_votes(player, vote)
        else:
            print(f"Invalid vote: {vote}. Vote must be a single alphabetic, numeric character, or 'GOODBYE'.")