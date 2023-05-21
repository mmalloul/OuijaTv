import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints.host import host
from endpoints.join import join

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Worstd"}

app.websocket("/host")(host)
app.websocket("/join")(join)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
