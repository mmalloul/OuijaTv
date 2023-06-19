from fastapi import APIRouter
from library.model.Game import Game
from global_state import active_games

router = APIRouter()

@router.post("/twitch/start")
async def start_bot(channel_name: str, room_token: str):
    try:
        game = Game(channel_name, room_token)
        active_games.update({room_token: game})
        await game.run_bot()

        return {"message": f"Joined Channel {channel_name}"}
    except Exception as e:
        return {"message": f"Failed to join Channel {channel_name}: {str(e)}"}
