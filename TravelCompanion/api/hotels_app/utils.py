from pydantic import BaseModel, Field

class HotelFilter(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(1, ge=1, le=100)

class HotelResponse(BaseModel):
    status: str
    results: dict


def get_params(query: str, limit: int) -> dict:
    return {
        "query": query,
        "limit": limit,
    }

def filter_hotel_data(data: dict) -> dict:
    return {
        "status": data.get("status"),
        "results": {
            "hotels": data.get("results", {}).get("hotels", [])
        }
    }
