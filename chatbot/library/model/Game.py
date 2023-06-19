from library.model.Bot import Bot

class Game:
    """
    A class representing a game.

    Attributes:
    - channel_name: Twitch Channel Name.
    - room_token: The token for the game room.
    - active_players: A list of active players in the game.
    - bot: The bot instance for the game.
    """

    def __init__(self, channel_name, room_token):
        self.room_token = room_token
        self.active_players = []
        self.channel_name = channel_name
        self.bot = Bot(channel_name, room_token, self)

    async def join_game(self, player):
        """
        Join the game with a player.

        Parameters:
        - player: The player object that joins the game.
        """
        if self.is_player_new(player):
            print(f"Twitch player joining game...")
            self.add_player(player)
            await player.join_game()
        else:
            print(f"Twitch player already joined.")

    async def player_votes(self, player, vote):
        """
        Send a vote from a player.

        Parameters:
        - player: The player object sending the vote.
        - vote: The vote value.

        Calls the player's send_vote method.
        """
        await player.send_vote(vote)

    def add_player(self, player):
        """
        Add a player to the active players list.

        Parameters:
        - player: The player object to add to the active player list.
        """
        self.active_players.append(player)

    def remove_player(self, player):
        """
        Remove a player from the active players list.

        Parameters:
        - player: The player object to remove from the active player list.
        """
        if player:
            self.active_players.remove(player)

    def is_player_new(self, player):
        """
        Check if a player is new.

        Returns:
        - True if the player is new, False otherwise.
        """
        return not any(active_player.name == player.name for active_player in self.active_players)

    def get_player_by_name(self, player_name):
        """
        Get a player by their name.

        Returns:
        - The player object if found, None otherwise.
        """
        return next((player for player in self.active_players if player.name == player_name), None)
    
    async def run_bot(self):
        """
        Run the bot.
        """
        try:
            print(f"Starting bot with room token: {self.room_token} and channel name: {self.channel_name}")
            await self.bot.run()
        except Exception as e:
            print(f"Error running bot: {str(e)}")

    async def stop_bot(self):
        """
        Stop the bot.
        """
        try:
            print(f"Stopping bot...")
            await self.bot.close()
        except Exception as e:
            print(f"Error stopping bot: {str(e)}")
