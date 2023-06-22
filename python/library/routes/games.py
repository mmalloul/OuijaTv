from fastapi import APIRouter, HTTPException
from library.stores.games import items as games


router = APIRouter()


# Endpoint for getting all game data
@router.get("/games")
async def get_all_games():
    return [
        {
            "pin": key,
            "players": [
                {
                    "name": player.name,
                    "voted": player.voted,
                }
                for player in game.players
            ],
            "name": game.name,
            "voting_time": game.voting_time,
            "game_mode": game.game_mode,
            "twitch_channel": game.twitch_channel,
        }
        for key, game in games.items()
    ]

# Endpoint to retrieve game by specific pin.
@router.get("/games/{pin}")
async def get_game_by_pin(pin: str):
    if pin in games:
        game = games[pin]
        return {
            "pin": pin,
            "players": [
                {
                    "pid": player.pid,
                    "name": player.name,
                    "voted": player.voted,
                }
                for player in game.players
            ],
            "name": game.name,
            "voting_time": game.voting_time,
            "game_mode": game.game_mode,
            "twitch_channel": game.twitch_channel,
        }
    else:
        raise HTTPException(status_code=404, detail="Game not found")