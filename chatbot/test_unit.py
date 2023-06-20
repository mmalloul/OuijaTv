import unittest

from unittest.mock import MagicMock
from unittest.mock import AsyncMock

from library.model.Game import Game
from library.model.Bot import Bot
from library.model.GameSession import GameSession
from library.model.Player import Player
from library.model.WebSocketClient import WebSocketClient

class TestGameSession(unittest.TestCase):
    def setUp(self):
        # arrange mock data
        self.game: Game = MagicMock(spec=Game)
        self.bot: Bot = MagicMock(spec=Bot)
        self.game_session: GameSession = GameSession(self.game, self.bot)

    async def test_run_bot(self):
        # act 
        await self.game_session.run_bot()

        # assert
        self.assertFalse(self.bot.run.awaited.has_exception())

    async def test_stop_bot(self):
        # act
        await self.game_session.stop_bot()

        # assert
        self.bot.close.assert_awaited()
        self.assertFalse(self.bot.close.awaited.has_exception())

class TestGame(unittest.TestCase):
    def setUp(self):
        # arrange mock data
        self.game = Game("channel_name", "room_token")
        self.websocket_client: WebSocketClient = MagicMock(spec=WebSocketClient)
        self.player: Player = MagicMock(spec=Player)
        self.player.name: str = "Mohammed Mock"
        self.player.websocket_client: WebSocketClient = self.websocket_client

    async def test_connect_player_to_game(self):
        # arrange
        self.websocket_client.connect = AsyncMock()

        # act
        await self.game.connect_player_to_game(self.player)

        # assert
        self.websocket_client.connect.assert_awaited()

    async def test_player_votes(self):
        # arrange
        self.websocket_client.send_message = AsyncMock()

        # act
        await self.game.player_votes(self.player, "A")

        # assert
        self.websocket_client.send_message.assert_awaited()

    def test_is_player_new(self):
        # arrange
        self.game.active_players.append(self.player)
        new_player = MagicMock(spec=Player)
        new_player.name = self.player.name

        # act
        result = self.game.is_player_new(new_player)

        # assert
        self.assertFalse(result)

    def test_add_player_to_active_player_list(self):
        # act
        self.game.add_player_to_active_player_list(self.player)

        # assert
        self.assertIn(self.player, self.game.active_players)

    def test_remove_player_from_active_players_list(self):
        # arrange
        self.game.active_players.append(self.player)

        # act
        self.game.remove_player_from_active_players_list(self.player)

        # assert
        self.assertNotIn(self.player, self.game.active_players)

    def test_get_player_by_name(self):
        # arrange
        self.game.active_players.append(self.player)

        # act
        result = self.game.get_player_by_name(self.player.name)

        # assert
        self.assertEqual(result, self.player)


if __name__ == "__main__":
    unittest.main()
