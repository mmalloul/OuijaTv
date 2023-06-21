from fastapi import APIRouter, HTTPException
from library.data.global_state import game_sessions
from library.model.Game import Game
from library.model.Bot import Bot
from library.model.GameSession import GameSession

router = APIRouter()

@router.post("/twitch/start")
async def start_bot(channel_name: str, room_token: str):
    """
    Start the Twitch bot for a specific channel and game room.

    Parameters:
    - channel_name: The name of the Twitch channel.
    - room_token: The token of the game room.

    Returns:
    - A message indicating the status of the bot start operation.
    """
    game_session = create_game_session(channel_name, room_token)
    await game_session.run_bot()

    print(f"Created game session with room token: {room_token} and channel name: {channel_name}")
    game_sessions[room_token] = game_session

    return {"message": f"Game session created for channel: {channel_name}"}

def create_game_session(channel_name: str, room_token: str) -> GameSession:
    """
    Creates an instance of a GameSession.

    Parameters:
    - channel_name: The name of the Twitch channel.
    - room_token: The token of the game room.

    Returns:
    -  An instance of a GameSession.
    """
    game = Game(channel_name, room_token)
    bot = Bot(channel_name, game)

    return GameSession(game, bot)
