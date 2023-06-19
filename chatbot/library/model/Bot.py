from twitchio.ext import commands
from library.model.Player import Player
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

    def __init__(self, channel_name: str, room_token: str, game):
        """
        Initialize the Bot object.

        Parameters:
        - channel_name: The name of the Twitch channel.
        - room_token: The token for the game room.
        - game: The game object associated with the bot.
        """
        print(f"Initializing bot with channel name: {channel_name} and room token: {room_token}")
        super().__init__(token=self.token, prefix='!', initial_channels=[channel_name])
        self.room_token = room_token
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

            # Extracting the vote from the message
            message_content = message.content.strip().upper()

            # Check if the message is a vote or play message
            if message_content.startswith('!'):
                player = self.game.get_player_by_name(name)

                if player is None:
                    player = Player(name, self.game)

                message_content = message_content[1:]  # Remove the exclamation mark

                print(f"New message from {name}: {message_content}")

                if message_content == self.play:
                    await self.game.join_game(player)
                else:
                    await self.process_vote(player, message_content)

    async def process_vote(self, player, vote):
        """
        Process a vote message.

        Parameters:
        - player: The Player object associated with the vote.
        - vote: The vote value.

        Checks if the vote is valid and passes it to the game object.
        Vote must be a single alphabetic, numeric character, or 'GOODBYE'.
        """
        if (vote in ascii_uppercase or vote in digits) or vote == self.goodbye:
            await self.game.player_votes(player, vote)
        else:
            print(f"Invalid vote: {vote}. Vote must be a single alphabetic, numeric character, or 'GOODBYE'.")
