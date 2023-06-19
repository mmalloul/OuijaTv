import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from library import routes

app = FastAPI()

origins = [
    "ouija.tv",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.include_router(routes.start)
app.include_router(routes.stop)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=25565)