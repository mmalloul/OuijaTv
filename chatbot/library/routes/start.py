from fastapi import APIRouter
from library.model.Game import Game
from global_state import active_games

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
    try:
        game = Game(channel_name, room_token)
        active_games.update({room_token: game})
        
        await game.run_bot()

        return {"message": f"Joined Channel {channel_name}"}
    except Exception as e:
        return {"message": f"Failed to join Channel {channel_name}: {str(e)}"}