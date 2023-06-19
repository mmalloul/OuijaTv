from library.model.Bot import Bot

class Game:
    def __init__(self, channel_name, room_token):
        self.GOODBYE = 'goodbye'
        self.room_token = room_token
        self.active_players = []
        self.channel_name = channel_name
        self.bot = Bot(channel_name, room_token, self)

    async def join_game(self, player):
        if self.is_player_new(player):
            print('Twitch player joining game...')
            self.add_player(player)
            await player.join_game()
        else:
            print('Twitch player already joined.')

    async def player_votes(self, player, vote):
        await player.send_vote(vote)

    def add_player(self, player):
        self.active_players.append(player)

    def remove_player(self, player):
          if player:
            self.active_players.remove(player)

    def is_player_new(self, player):
        for active_player in self.active_players:
            if active_player.name == player.name:
                return False
        return True
    
    def get_player_by_name(self, name):
        for player in self.active_players:
            if player.name == name:
                return player
        print('Player does not exist')
        return None

    async def run_bot(self):
        print(f"Starting bot with room token: {self.room_token}  and channel name: " + self.channel_name)
        await self.bot.run()

    async def stop_bot(self):
        print("Stopping bot...")
        await self.bot.close()
