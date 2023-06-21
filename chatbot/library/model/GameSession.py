from library.model.Game import Game
from library.model.Bot import Bot

class GameSession:
    """
    A class representing a game session in the game.
    ...
    """
    def __init__(self, game: Game, bot: Bot):
        self.game = game
        self.bot = bot
    
    async def run_bot(self):
        """
        Run the bot.
        ...
        """
        try:
            print(f"Starting bot with room token: {self.game.room_token} and channel name: {self.game.channel_name}")
            await self.bot.run()
        except Exception as e:
            print(f"Error running bot: {str(e)}")

    async def stop_bot(self):
        """
        Stop the bot.
        ...
        """
        try:
            print(f"Stopping bot...")
            await self.bot.close()
        except Exception as e:
            print(f"Error stopping bot: {str(e)}")