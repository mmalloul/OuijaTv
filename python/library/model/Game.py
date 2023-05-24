from dataclasses import dataclass
from fastapi import WebSocket
from string import ascii_uppercase, digits
from python.library.model.MessageType import ServerMessageType
from python.library.model.Player import Player
from python.library.model.Message import Message


@dataclass
class Game:
    host: WebSocket
    players: list[Player] = list()
    votes: dict[str, int] = dict()
    prompt: str = ""

    def __post_init__(self) -> None:
        """Initialise vote dictionary."""

        if not self.votes:
            options = [*(ascii_uppercase + digits), "GOODBYE"]
            self.votes = {option: 0 for option in options}


    def subscribe(self, player: Player) -> None:
        """Add a player to the game."""

        self.players.append(player)


    def find_player(self, socket: WebSocket) -> Player | None:
        """Find a player through their socket."""

        matching_players = (player for player in self.players if player.socket == socket)
        return next(matching_players, None)


    async def notify_host(self, message: Message[ServerMessageType]) -> None:
        """Send a message to the host."""

        await self.host.send_json(message)


    async def broadcast_players(self, message: Message[ServerMessageType]) -> None:
        """Send a message to all players in the game."""

        for player in self.players:
            await player.socket.send_json(message)