from dataclasses import dataclass, field
from fastapi import WebSocket
from string import ascii_uppercase, digits
from library.model.MessageType import ServerMessageType
from library.model.Player import Player
from library.model.Message import ServerMessage


@dataclass
class Game:
    """Equivalent to a "vesel", "room", or "lobby"."""
    
    host: WebSocket
    players: list[Player] = field(default_factory=list)
    votes: dict[str, int] = field(default_factory=dict)
    prompt: str = ""
    

    def __post_init__(self) -> None:
        """Initialise vote dictionary."""

        if not self.votes:
            options = [*(ascii_uppercase + digits), "GOODBYE"]
            self.votes = {option: 0 for option in options}


    def join(self, player: Player) -> None:
        """Add a player to the game."""

        self.players.append(player)


    def find_player(self, socket: WebSocket) -> Player | None:
        """Find a player through their socket."""

        matching_players = (player for player in self.players if player.socket == socket)
        return next(matching_players, None)


    async def restart(self) -> None:
        """Set all votes to 0, clear prompt, and notify players."""

        # reset votes
        for vote in self.votes:
            self.votes[vote] = 0

        # prepare messages
        message_restart = ServerMessage(ServerMessageType.RESTART)
        message_votes = ServerMessage(ServerMessageType.VOTE, self.votes)

        await self.broadcast(message_restart)
        await self.broadcast(message_votes)


    async def notify_host(self, message: ServerMessage) -> None:
        """Send a message to the host."""

        await self.host.send_json(message.json)


    async def notify_player(self, player: Player, message: ServerMessage) -> None:
        """Send a message to a player."""

        await player.socket.send_json(message.json)
    

    async def broadcast(self, message: ServerMessage) -> None:
        """Send a message to all sockets."""

        for player in self.players:
            await player.socket.send_json(message.json)

        await self.host.send_json(message.json)
