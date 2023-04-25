import uvicorn
from fastapi import FastAPI
from endpoints.host import host
from endpoints.join import join

app = FastAPI()

app.websocket("/host")(host)
app.websocket("/join")(join)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
