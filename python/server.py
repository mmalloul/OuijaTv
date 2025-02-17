import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from library import routes
from library.stores.games import items as games

app = FastAPI()

origins = [
    "https://ouija.tv",
    "https://staging.ouija.tv",
    "https://www.ouija.tv",
    "https://www.staging.ouija.tv",
    "wss://www.ouija.tv",
    "wss://www.staging.ouija.tv",
    "wss://ouija.tv",
    "wss://staging.ouija.tv",
    "http://www.ouija.tv:25565",
    "https://www.ouija.tv:25565",
    "http://ouija.tv:25565",
    "https://ouija.tv:25565",
    "http://www.ouija.tv:25566",
    "https://www.ouija.tv:25566",
    "http://ouija.tv:25566",
    "https://ouija.tv:25566",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.include_router(routes.host)
app.include_router(routes.join)
app.include_router(routes.openai)
app.include_router(routes.games)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
