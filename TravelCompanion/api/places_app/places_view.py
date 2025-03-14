from fastapi import APIRouter, Query
import requests
from api.places_app.config import url, headers, LIMIT
from api.places_app.utils import query

router = APIRouter()


@router.get("/places/names/")
def read_name_places(name: str, city: str, country: str = 'Morocco', limit: int = LIMIT) -> dict:
    """Отображает места по названиям."""
    response = requests.get(
        url=url,
        headers=headers,
        params=query(parameter=name, city=city, country=country, limit=limit)
    )
    
    if response.status_code != 200:
        return {
            "error": "Failed to fetch data from Foursquare API",
            "status_code": response.status_code,
            "response_text": response.text,
        }
    
    return response.json()
    
    
@router.get("/places/categories/")
def read_categories_places(category: str, city: str, country: str = 'Morocco', limit: int = LIMIT) -> dict:
    """Отображает места по категориям."""
    response = requests.get(
        url=url,
        headers=headers,
        params=query(parameter=category, city=city, country=country, limit=limit)
    )
    
    if response.status_code != 200:
        return {
            "error": "Failed to fetch data from Foursquare API",
            "status_code": response.status_code,
            "response_text": response.text,
        }
    
    return response.json()
    
