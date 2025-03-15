from fastapi import APIRouter, Query, HTTPException, status
import requests
import json
from api.places_app.config import url, headers, LIMIT
from api.places_app.utils import query, save_api_response
from typing import Union


router = APIRouter()

@router.get("/places/names/")
def read_name_places(name: str, city: str, country: str = 'Morocco', limit: int = LIMIT) -> dict:
    """Отображает места по названиям."""
    response = requests.get(
        url=url,
        headers=headers,
        params=query(parameter=name, city=city, country=country, limit=limit)
    )
        
    json_response = response.json()
    
    # Сохраняем ответ в файл
    try:
        save_api_response(json_response)
    except Exception as e:
        print(f"Ошибка при сохранении ответа: {str(e)}")
    
    return json_response
    #return response.json()
    
    
@router.get("/places/categories/")
def read_categories_places(category: str, city: str, country: str = 'Morocco', limit: int = LIMIT) -> dict:
    """Отображает места по категориям."""
    response = requests.get(
        url=url,
        headers=headers,
        params=query(parameter=category, city=city, country=country, limit=limit)
    )

    json_response = response.json()
    
    # Сохраняем ответ в файл
    try:
        save_api_response(json_response)
    except Exception as e:
        print(f"Ошибка при сохранении ответа: {str(e)}")
    
    return json_response
    #return response.json()
    
