from fastapi import APIRouter

router = APIRouter()

@router.get("/hotels/")
async def read_hotels():
    return {"message": "List of hotels"}
