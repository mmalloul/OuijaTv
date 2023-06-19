from fastapi import APIRouter
from library.model.Game import Game
from global_state import active_games

router = APIRouter()

@router.post("/twitch/stop")
async def stop_bot(room_token: str):
    """
    Stop the Twitch bot for a specific game room.

    Parameters:
    - room_token: The token of the game room.

    Returns:
    - A message indicating the status of the bot stop operation.
    """
    try:
        game = active_games.pop(room_token, None)

        if game:
            await game.stop_bot()
            return {"message": f"Stopped bot in Room {room_token}"}
        else:
            return {"message": f"Failed to stop bot in Room {room_token}: Game not found"}
    except Exception as e:
        return {"message": f"Failed to stop bot in Room {room_token}: {str(e)}"}
