import requests

from api.hotels_app.config import url
from api.hotels_app.utils import (HotelFilter, HotelResponse, filter_hotel_data,
                                  get_params)
from fastapi import APIRouter, Depends, HTTPException, Query


router = APIRouter()

@router.get('/hotels/', response_model=HotelResponse)
def read_hotels(
    query: str = Query(..., min_length=1),
    limit: int = Query(1, ge=1, le=20)
):
    filter_params = HotelFilter(query=query, limit=limit)
    params = get_params(filter_params.query, filter_params.limit)
    response = requests.get(url=url, params=params)
    
    
    data = response.json()
    filtered_data = filter_hotel_data(data)
    return filtered_data
