import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints.host import host
from endpoints.join import join
from endpoints.ai import openai_call
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Worstd"}



# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://ouija.tv"],  # Add the origin of your Svelte application
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

@app.get("/openai")
async def ai_call(prompt: str, spirit:int):
    print(prompt)
    print(spirit)
    response = await openai_call(prompt, spirit)
    return response

app.websocket("/host")(host)
app.websocket("/join")(join)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('BACKEND_PORT')))
    
