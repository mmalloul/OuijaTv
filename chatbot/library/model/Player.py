import websockets
from dotenv import load_dotenv
import os
import json
from library.model.MessageType import MessageType

# Load variables from .env file
load_dotenv('../.env')

class Player:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.websocket = None 
        self.can_vote: bool = False

    async def join_game(self):
        try:
            base_url = os.getenv('PUBLIC_WS_URL')
            url = base_url + '/join?pin=' + self.game.room_token + '&username=' + self.name
            self.websocket = await websockets.connect(url)
            print("WebSocket connected.")
            
            await self.receive_messages()

        except websockets.WebSocketException as e:
            print(f"Error connecting to WebSocket: {e}")

    async def receive_messages(self):
        try:
            while True:
                message = await self.websocket.recv()
                message = json.loads(message)
                print(message)

                match message['type']:
                    case MessageType.RESTART.value:
                        self.can_vote = False
                    
                    case MessageType.PROMPT.value:
                        print('prompt requested')
                        self.can_vote = True
   
                    case MessageType.WINNING_VOTE.value:
                        print('prompt requested')
                        self.can_vote = False

                    case MessageType.QUIT.value:
                        self.can_vote = False
                        print("Connection closed by the server.")
                        self.game.remove_player(self)
                        self.websocket.close()

        except Exception as e:
            print(f"Error occurred: {str(e)}")
        
    async def send_vote(self, vote):
        print(self.check_websocket, self.can_vote)
        if self.check_websocket() and self.can_vote:
            print('send vote')
            message = json.dumps({
                "type": "vote",
                "content": vote,
            })

            await self.websocket.send(message)

    def check_websocket(self):
        if self.websocket is None:
            print("Websocket is not initialized. Player needs to join the game first.")
            return False
        else:
            return True
