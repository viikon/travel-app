from fastapi import FastAPI
import requests
import json
from collections import defaultdict
from api.places_app.places_view import router as places_router
from api.hotels_app.hotels_views import router as hotels_router
from api.places_app.config import url, headers, LIMIT
from api.places_app.utils import get_popular_category, query_recomend

app = FastAPI()

app.include_router(places_router, prefix="/api")
app.include_router(hotels_router, prefix="/api")


@app.get("/")
def home():
    return {"message" : "Welcome to TravelCompanion!"}
    

@app.get("/recomend/")
def read_recomend(city: str, country: str = 'Morocco', limit: int = LIMIT) -> dict:

    response = requests.get(
        url=url,
        headers=headers,
        params=query_recomend(city=city, country=country, limit=limit)
    )
    
    if response.status_code != 200:
        return {
            "error": "Failed to fetch data from Foursquare API",
            "status_code": response.status_code,
            "response_text": response.text,
        }
    
    return response.json()
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
