import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from library import routes
from library.stores.games import items as games

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    # TODO ONLY ALLOW OUR ORIGINS. THIS TEMPORARY ALLOWS ALL, BUT HAS SECURITY RISKS
    allow_origins=["*"], 
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


app.include_router(routes.host)
app.include_router(routes.join)
app.include_router(routes.openai)

# Endpoint for getting all game data
@app.get("/games")
def get_all_games():
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
            "game_mode": game.game_mode
        }
        for key, game in games.items()
    ]

# Endpoint to retrieve game by specific pin.
@app.get("/games/{pin}")
def get_game_by_pin(pin: str):
    if pin in games:
        game = games[pin]
        return {
            "pin": pin,
            "players": [
                {
                    "name": player.name,
                    "voted": player.voted,
                }
                for player in game.players
            ],
            "name": game.name,
            "voting_time": game.voting_time,
            "game_mode": game.game_mode
        }
    else:
        raise HTTPException(status_code=404, detail="Game not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
