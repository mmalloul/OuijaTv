from fastapi import FastAPI
from python.library import routes


app = FastAPI()

app.include_router(routes.host)
app.include_router(routes.join)
app.include_router(routes.openai)