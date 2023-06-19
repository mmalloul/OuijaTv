from fastapi import APIRouter
from global_state import active_games

router = APIRouter()

@router.post("/twitch/stop")
async def stop_bot(room_token: str):
    try:
        game = active_games.pop(room_token, None)

        if game:
            await game.stop_bot()
            return {"message": f"Stopped bot in Room {room_token}"}
        else:
            return {"message": f"Failed to stop bot in Room {room_token}: Game not found"}
    except Exception as e:
        return {"message": f"Failed to stop bot in Room {room_token}: {str(e)}"}
