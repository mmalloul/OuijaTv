from fastapi import APIRouter

router = APIRouter()


@router.get("/openai")
async def host():
    return {"message": "Hello, openai!"}