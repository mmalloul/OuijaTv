from twitchio.ext import commands
from library.model.Player import Player
from string import ascii_uppercase, digits
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv('../.env')

class Bot(commands.Bot):
    client_id: str = os.getenv('TWITCH_CLIENT_ID')
    token: str = os.getenv('TWITCH_TOKEN')
    play: str = 'PLAY'

    def __init__(self, channel_name: str, room_token: str, game):
        print(f"Initializing bot with room token: {room_token}  and channel name: " + channel_name)
        super().__init__(token=self.token, prefix='!', initial_channels=[channel_name])
        self.game = game
        self.room_token = room_token 

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.author.name.lower() != self.nick.lower():
 
            name = message.author.name
            # Extracting the vote from the message
            message = message.content.strip().upper()

            # Check if the message is a vote or play message
            if message.startswith('!'):
                player = self.game.get_player_by_name(name)

                if (player == None):
                    player = Player(name, self.game)

                message = message[1:]  # Remove the exclamation mark

                print(f"New message from {name}: {message}")

                if (message == self.play):
                     await self.game.join_game(player)
                else:
                     await self.process_vote(player, message)

    async def process_vote(self, player, vote):
        if len(vote) == 1 and (vote in ascii_uppercase or vote in digits):
            await self.game.player_votes(player, vote)
        else:
            print(f"Invalid vote: {vote}. Vote must be a single alphabetic or numeric character.")
