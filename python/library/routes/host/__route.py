from fastapi import APIRouter

router = APIRouter()


@router.get("/host")
async def host():
    return {"message": "Hello, host!"}