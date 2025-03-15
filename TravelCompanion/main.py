from fastapi import FastAPI
import requests
import json
import sqlite3
from collections import defaultdict
from contextlib import contextmanager
from api.places_app.places_view import router as places_router
from api.hotels_app.hotels_views import router as hotels_router
from api.places_app.config import url, headers, LIMIT
from api.places_app.utils import get_popular_category, query_recomend, process_categories
from data_base.views import router as database_router
from data_base.config import db_helper, CreateTableHelper
from fastapi import Depends


@contextmanager
def get_database_session():
    connection = db_helper.engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    
    try:
        yield session
        transaction.commit()
    except Exception as e:
        transaction.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
        connection.close()

app = FastAPI()

app.include_router(places_router, prefix="/api")
app.include_router(hotels_router, prefix="/api")
app.include_router(database_router, prefix="/database")

@app.get("/")
def home():
    return {"message" : "Welcome to TravelCompanion!"}
    

@app.get("/recomend/")
def read_recomend(city: str, country: str = 'Morocco', limit: int = LIMIT) -> dict:
    process_categories()

    response = requests.get(
        url=url,
        headers=headers,
        params=query_recomend(city=city, country=country, limit=limit)
    )
    
    return response.json()
    
if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", port=8000, reload=True)
