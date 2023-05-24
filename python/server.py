import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from library import routes

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
