from enum import Enum

import requests
from fastapi import APIRouter, HTTPException, Query, status

from api.places_app.config import settings
from api.places_app.utils import handle_saving_response, save_api_response, query



class StaticCategory(str, Enum):
    food = "Restaurant"
    attraction = "Museum"
    shopping = "Store"
    monuments = "Monument"
    cafés = "Café"
    bars = "Bar"
    gastropubs = "Gastropub"


router = APIRouter()
        

@router.get("/places/names/")
def read_name_places(name: str, city: str, country: str = 'Morocco', limit: int = settings.limit) -> dict:
    """Отображает места по названиям."""
    response = requests.get(
        url=settings.foursquare_url,
        headers=settings.headers,
        params=query(parameter=name, city=city, country=country, limit=limit)
    )
        
    json_response = response.json()

    handle_saving_response(json_response)
    
    return json_response
    
    
@router.get("/places/categories/{category}")
def read_categories_places(category: StaticCategory, city: str, country: str = 'Morocco', limit: int = settings.limit) -> dict:
    """Отображает места по категориям."""
    response = requests.get(
        url=settings.foursquare_url,
        headers=settings.headers,
        params=query(parameter=category.value, city=city, country=country, limit=limit)
    )

    json_response = response.json()
    
    handle_saving_response(json_response)
    
    return json_response

    
