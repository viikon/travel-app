import requests
from fastapi import FastAPI

from api.places_app.places_view import router as places_router
from api.hotels_app.hotels_views import router as hotels_router
from api.places_app.config import settings
from api.places_app.utils import get_popular_category, process_categories, query_recomend
from data_base.config import CreateTableHelper, db_helper
from data_base.views import router as database_router


app = FastAPI()

app.include_router(places_router, prefix="/api")
app.include_router(hotels_router, prefix="/api")
app.include_router(database_router, prefix="/database")


@app.get("/")
def home():
    return {"message" : "Welcome to TravelCompanion!"}
    

@app.get("/recomend/")
def read_recomend(city: str, country: str = 'Morocco', limit: int = settings.limit) -> dict:
    process_categories()

    response = requests.get(
        url=settings.foursquare_url,
        headers=settings.headers,
        params=query_recomend(city=city, country=country, limit=limit)
    )
    
    return response.json()
    
if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", port=8000, reload=True)
