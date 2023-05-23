import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoints.host import host
from .endpoints.join import join
from .endpoints.ai import openai_call

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://ouija.tv"],  # Add the origin of your Svelte application
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

@app.get("/")
async def root():
    return "Ouija.TV API root"

@app.get("/openai")
async def ai_call(prompt: str, spirit:int):
    response = await openai_call(prompt, spirit)
    return response

app.websocket("/host")(host)
app.websocket("/join")(join)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
