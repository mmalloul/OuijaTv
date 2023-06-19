import websockets
from dotenv import load_dotenv
import os
import json
from library.model.MessageType import MessageType

# Load variables from .env file
load_dotenv('../.env')

class Player:
    """
    A class representing a player in the game.

    Attributes:
    - name: The name of the player.
    - game: The game object the player is associated with.
    - websocket: The WebSocket connection for the player.
    - can_vote: A boolean indicating if the player can vote.
    """

    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.websocket = None
        self.can_vote = False

    async def join_game(self):
        """
        Join the game.

        Establishes a WebSocket connection with the game server and starts receiving messages.
        """
        try:
            url = f"{os.getenv('PUBLIC_WS_URL')}/join?pin={self.game.room_token}&username={self.name}"

            self.websocket = await websockets.connect(url)
            print("WebSocket connected.")

            await self.receive_messages()

        except websockets.WebSocketException as e:
            print(f"Error connecting to WebSocket: {e}")

    async def receive_messages(self):
        """
        Receive messages from the game server.

        Continuously receives messages from the WebSocket connection.
        This can be used to add logic to our code where needed.
        Currently its being used for the van_vote boolean.
        """
        try:
            while True:
                message = await self.websocket.recv()
                message = json.loads(message)
                print(message)

                match message["type"]:
                    case MessageType.RESTART.value:
                        self.can_vote = False
                    
                    case MessageType.PROMPT.value:
                        self.can_vote = True
   
                    case MessageType.WINNING_VOTE.value:
                        self.can_vote = False

                    case MessageType.QUIT.value:
                        self.can_vote = False
                        print(f"Connection closed by the server.")
                        self.game.remove_player(self)
                        self.websocket.close()


        except Exception as e:
            print(f"Error occurred: {str(e)}")

    async def send_vote(self, vote):
        """
        Send a vote to the game server.

        Parameters:
        - vote: The vote value to send.

        Sends the vote as a JSON message to the game server if the player is allowed to vote.
        """
        if self.check_websocket() and self.can_vote:
            print(f"sending vote: {vote}")

            message = json.dumps({
                "type": "vote",
                "content": vote,
            })

            await self.websocket.send(message)

    def check_websocket(self):
        """
        Check if the WebSocket connection is initialized.
        """
        if self.websocket:
            return True
        else:
            print(f"Websocket is not initialized. Player needs to join the game first.")
            return False
