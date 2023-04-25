from fastapi import FastAPI
from endpoints.host import host
from endpoints.join import join

app = FastAPI()

app.websocket("/host")(host)
app.websocket("/join")(join)
