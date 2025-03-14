from fastapi import APIRouter, Query
import requests
from api.hotels_app.config import url
from api.hotels_app.utils import get_params, filter_hotel_data

router = APIRouter()  # Добавляем префикс для роутера


@router.get('/hotels/')
def read_hotels(query: str = "Khanuma Hotel", limit: int = Query(default=1)):
    params = get_params(query, limit)
    
    response = requests.get(url=url, params=params)
    
    if response.status_code != 200:
        return {
            "error": "Failed to fetch data from external API",
            "status_code": response.status_code,
            "response_text": response.text,
        }
        
    data = response.json()
    filtered_data = filter_hotel_data(data)
    
    return filtered_data
   
