from fastapi import APIRouter

router = APIRouter()


@router.get("/join")
async def host():
    return {"message": "Hello, join!"}