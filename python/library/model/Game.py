import asyncio
from dataclasses import dataclass, field
from fastapi.websockets import WebSocketState
from fastapi import WebSocket
from typing import Optional
from string import ascii_uppercase, digits
from library.model.MessageType import ServerMessageType
from library.model.Player import Player
from library.model.Message import ServerMessage
from library.model.VoteData import VoteData
from dotenv import load_dotenv
import os
import requests

# Load variables from .env file
load_dotenv('../../.env')

@dataclass
class Game:
    """Equivalent to a "vesel", "room", or "lobby"."""
    host: WebSocket
    players: list[Player] = field(default_factory=list)
    prompt: str = ""
    GOODBYE: str = "!" # In the svg the goodbye button id = "!".
    word: str = ""
    name: str = ""
    votes: dict[str, VoteData] = field(default_factory=dict)   
    vote_id: int = 0
    voting_time: int = 0
    game_mode: str = ""
    twitch_channel: str = ""
    winning_letter: str = ""
    no_vote_streak: int = 0
    stop_threshold: int = 3
    countdown_task: Optional[asyncio.Task] = None

    def __post_init__(self) -> None:
        """Initialise vote dictionary."""

        if not self.votes:
            options = [*(ascii_uppercase + digits), self.GOODBYE]
            self.votes = {option: VoteData(0,0) for option in options}

    def join(self, player: Player) -> None:
        """Add a player to the game."""

        self.players.append(player)

    def find_player(self, socket: WebSocket) -> Player | None:
        """Find a player through their socket."""

        matching_players = (player for player in self.players if player.socket == socket)
        return next(matching_players, None)


    def start_countdown(self) -> None:
        """Start counting down."""

        if self.countdown_task:
            self.countdown_task.cancel()

        self.countdown_task = asyncio.create_task(self.countdown())

    def reset_votes(self) -> None:
        """Reset all votes to zero while keeping their keys."""

        for vote in self.votes:
            self.votes[vote] = VoteData(0, 0)

        for player in self.players:
            player.voted = False

        self.vote_id = 0
            

    async def vote(self, vote: str, player: Player) -> None:
        """Add a vote to the game."""

        if vote in self.votes and not player.voted:

            player.voted = True
            
            voteData = self.votes[vote]
            print(self.vote_id)
            self.votes[vote] = VoteData(voteData.count + 1, self.vote_id)
            self.vote_id += 1
            print(self.votes)

            # Determine the new winning letter by looking at the highest voteData.count in self.votes
            # If there are multiple letters with the same voteData.count, pick the one with the highest self.vote_id.
            new_winning_letter = max(self.votes, key=lambda x: (self.votes[x].count, self.votes[x].id))


            if (self.winning_letter != new_winning_letter):
                self.winning_letter = new_winning_letter
                await self.broadcast(
                    ServerMessage(
                        ServerMessageType.WINNING_VOTE, 
                        self.winning_letter
                    )
                )

            await self.notify_host(
                ServerMessage(
                    ServerMessageType.VOTE, 
                    self.votes,
                ),
            )

    async def countdown(self) -> None:
        """Count down, notifying the host every second."""

        count = self.voting_time
        while count > -1:
            await asyncio.sleep(1)
            await self.broadcast(
                ServerMessage(
                    ServerMessageType.COUNTER, 
                    count,
                ),
            )
            count -= 1
        await self.pick_letter()

    async def pick_letter(self) -> None:
        """Adds most popular letter to word, notify all clients, and reset votes."""

        isZeroVotes = all(value == 0 for value in self.votes.values())
        
        if (isZeroVotes):
            self.no_vote_streak += 1

            await self.broadcast(
                ServerMessage(ServerMessageType.NO_VOTES)
            )

            if self.no_vote_streak == self.stop_threshold:
                if self.countdown_task:  
                    self.countdown_task.cancel()

                    await self.broadcast(
                        ServerMessage(
                            ServerMessageType.STOP_COUNTDOWN,
                        )
                    ) 
                    return

                self.no_vote_streak = 0
        else:
            self.no_vote_streak = 0
            
            winning_option = max(self.votes, key=lambda x: (self.votes[x].count, self.votes[x].id))

            if winning_option == self.GOODBYE:
                await self.broadcast(
                    ServerMessage(
                        ServerMessageType.WORD, 
                        winning_option
                    )
                )
                return

            self.word += winning_option

        self.start_countdown()
        
        await self.broadcast(
            ServerMessage(
                ServerMessageType.WORD,
                self.word,
            ),
        )

        self.reset_votes()

    async def restart(self) -> None:
        """Set all votes to zero, clear prompt, and notify players."""

        self.reset_votes()
        self.word = ""
        self.prompt = ""

        # Cancel the countdown task if it's running
        if self.countdown_task:  
            self.countdown_task.cancel()

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
    

    async def broadcast(self, message: ServerMessage, notify_host=True) -> None:
        """Send a message to all sockets."""
        
        for player in self.players:
            if player.socket.client_state == player.socket.application_state == WebSocketState.CONNECTED:
                await player.socket.send_json(message.json)

        if notify_host:
            await self.host.send_json(message.json)

    async def start_twitch_bot(self, twitch_channel, pin):
        if twitch_channel != None:
            url = f"{os.getenv('PUBLIC_TWITCH_URL')}/twitch/start?channel_name={twitch_channel}&room_token={pin}"
            requests.post(url)

            return {"message": f"Requesting chatbot server to start bot in room: {pin}"}
        else:
            return {"message": f"No twitch_channel provided"}