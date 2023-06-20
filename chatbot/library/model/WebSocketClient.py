import websockets

class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.url)
        print(f"WebSocket connected.")

    async def receive_messages(self):
        """
        Receives messages from the game server.
        """
        try:
            while True:
                message = await self.websocket.recv()
                print(f"Received message: {message}")
        except websockets.ConnectionClosed:
            print(f"Connection closed.")
        except Exception as e:
            print(f"Error occurred: {str(e)}")

    async def send_message(self, message):
        """
        Send a message to the game server.
        ...
        """
        if self.check_websocket():
            await self.websocket.send(message)

    def check_websocket(self):
        """
        Check if the WebSocket connection is initialized.
        ...
        """
        if self.websocket:
            return True
        else:
            print(f"Websocket is not initialized. Player needs to join the game first.")
            return False
        
    async def close(self):
        """
        Disconnect from the WebSocket server.
        ...
        """
        if self.websocket:
            await self.websocket.close()