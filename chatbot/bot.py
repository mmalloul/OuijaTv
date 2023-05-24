from twitchio.ext import commands
from vote import Vote
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv('../.env')


class Bot(commands.Bot):
    client_id = os.getenv('TWITCH_CLIENT_ID')
    refresh_token = os.getenv('TWITCH_REFRESH_TOKEN')


    def __init__(self):
        super().__init__(token=os.getenv('TWITCH_TOKEN'), prefix='!', initial_channels=['thimsie'])
        self.vote_handler = Vote()

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.author.name.lower() != self.nick.lower():
            print(f"New message from {message.author.name}: {message.content}")

            # Extracting the vote from the message
            vote = message.content.strip().upper()

            # Process the vote or update the vote counts
            self.process_vote(vote)

    def process_vote(self, vote):
        # Implement your vote processing logic here
        if vote.startswith('!'):
            vote_option = vote[1:]  # Remove the exclamation mark
            self.vote_handler.updateVotes(vote_option)

    @commands.command()
    async def display_votes(self, ctx: commands.Context):
        # Display vote counts
        self.vote_handler.displayVotes()

bot = Bot()
bot.run()
