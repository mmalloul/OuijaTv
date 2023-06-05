import uvicorn
from fastapi import FastAPI
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

@app.get("/games")
def get_games():
    return [
        {
            "pin": key,
            "players": [
                {
                    "name": player.name,
                    "voted": player.voted,
                }
                for player in game.players
            ]
            #game.name 
        }
        for key, game in games.items()
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
