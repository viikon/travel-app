from fastapi import APIRouter

router = APIRouter()

@router.get("/places/")
async def read_places():
    return {"message": "List of places"}
