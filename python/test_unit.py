import unittest
from unittest.mock import MagicMock
from unittest.mock import AsyncMock

from library.model.Message import ServerMessage
from library.model.MessageType import ServerMessageType
from fastapi.websockets import WebSocketState
from library.model import Game

from library.stores.games import items as storesGames
from library.stores.games import new as newGame, remove as removeGame

import asyncio


class TestGame(unittest.TestCase):

    # why is this not following snake_case convention?
    def setUp(self):
        self.host_socket = AsyncMock()        
        self.host = AsyncMock()
        self.host.socket = self.host_socket
        self.game = Game(self.host)

    def test_join(self):
        player = MagicMock()
        self.game.join(player)
        self.assertEqual(len(self.game.players), 1)
        self.assertEqual(self.game.players[0], player)

    # happy path
    def test_find_player_existing(self):
        player = MagicMock()
        self.game.players.append(player)
        self.assertEqual(self.game.find_player(player.socket), player)

    # sad path
    def test_find_player_non_existing(self):
        player = MagicMock()
        self.assertIsNone(self.game.find_player(player.socket))

    def test_reset_votes(self):
        self.game.players = [MagicMock(voted=True), MagicMock(voted=True)]
        self.game.votes = {"A": 2, "B": 1}
        self.game.reset_votes()
        self.assertEqual(self.game.votes, {"A": 0, "B": 0})
        for player in self.game.players:
            self.assertFalse(player.voted)

    def test_notify_host(self):
        # Create a game with a mock host
        mock_host = AsyncMock()
        game = Game(mock_host)

        # Send a message
        test_message = ServerMessage(ServerMessageType.WINNING_VOTE)
        asyncio.run(game.notify_host(test_message))

        # Assert that the send_json method was called with the correct argument
        mock_host.send_json.assert_called_once_with(test_message.json)

    def test_notify_player(self):
        # Create a game with a mock host
        mock_host = AsyncMock()
        game = Game(mock_host)

        # Create a mock player to notify 
        mock_player = AsyncMock()
        mock_player.socket = AsyncMock()
        test_message = ServerMessage(ServerMessageType.WINNING_VOTE)

        asyncio.run(game.notify_player(mock_player, test_message))

        # Assert that the send_json method was called with the correct argument
        mock_player.socket.send_json.assert_called_once_with(test_message.json)

    def test_broadcast_all(self):
        # Create a list of mock players, and initialize their .socket property with an AsyncMock
        mock_players = [MagicMock() for _ in range(5)]
        for player in mock_players:
            player.socket = AsyncMock()
            player.socket.client_state = WebSocketState.CONNECTED
            player.socket.application_state = WebSocketState.CONNECTED

        self.game.players = mock_players

        # Create a mock player to notify 
        test_message = ServerMessage(ServerMessageType.WINNING_VOTE)

        asyncio.run(self.game.broadcast(test_message))

        # Assert that the send_json method was called with the correct argument
        for player in mock_players:
            player.socket.send_json.assert_called_once_with(test_message.json)
        self.game.host.send_json.assert_called_once_with(test_message.json)

    def test_broadcast_all_except_host(self):
        # Create a list of mock players, and initialize their .socket property with an AsyncMock
        mock_players = [MagicMock() for _ in range(5)]
        for player in mock_players:
            player.socket = AsyncMock()
            player.socket.client_state = WebSocketState.CONNECTED
            player.socket.application_state = WebSocketState.CONNECTED

        self.game.players = mock_players

        # Create a mock player to notify 
        test_message = ServerMessage(ServerMessageType.WINNING_VOTE)

        asyncio.run(self.game.broadcast(test_message, False))

        # Assert that the send_json method was called with the correct argument
        for player in mock_players:
            player.socket.send_json.assert_called_once_with(test_message.json)
        self.game.host.send_json.assert_not_called()
        

    def test_restart_game(self):
        self.game.word = "someWord"
        self.game.prompt = "somePrompt"

        self.game.countdown_task = MagicMock()
        asyncio.run(self.game.restart())
        
        self.game.countdown_task.cancel.assert_called_once()
        assert(self.game.word == "")
        assert(self.game.prompt == "")

    def test_message_json_conversion (self):
        message = ServerMessage(ServerMessageType.WINNING_VOTE)
        assert(message.json == {"type": "winningVote", "content": ""})


class TestGameStores (unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        storesGames.clear()
        return super().tearDown()
    
    def test_create_game(self):
        assert(len(storesGames) == 0)
        newGame(MagicMock(), "Test Game", "15", "Test Mode", 6)
        assert(len(storesGames) == 1)

    def test_remove_game_by_pin(self):
        assert(len(storesGames) == 0)
        game = newGame(MagicMock(), "Test Game", "15", "Test Mode", 6)
        pin = game[0]
        removeGame(pin)
        assert(len(storesGames) == 0)

    def test_remove_player_from_game(self):
        assert(len(storesGames) == 0)
        result = newGame(MagicMock(), "Test Game", "15", "Test Mode", 6)
        pin = result[0]
        game = result[1]
        mock_player = MagicMock()
        game.players.append(mock_player)

        assert(len(game.players) == 1)

        removeGame(pin, player=mock_player)
        assert(len(game.players) == 0)    



        

if __name__ == "__main__":
    unittest.main()
