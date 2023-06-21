from fastapi import APIRouter
from library.model.Game import Game
from library.data.global_state import game_sessions
from library.model.Game import Game
from library.model.Bot import Bot
from library.model.GameSession import GameSession
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
        game_session: GameSession = game_sessions.get(room_token)

        if game_session is None:
            return {"message": f"Game session not found for Room {room_token}"}

        await game_session.stop_bot()

        print(f"Deleting game session with room token: {game.room_token} and channel name: {game.channel_name}")
        del game_sessions[room_token]

        return {"message": f"Stopped bot in Room {room_token}"}

    except Exception as e:
        return {"message": f"Failed to stop bot in Room {room_token}: {str(e)}"}
