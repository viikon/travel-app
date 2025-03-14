import json
import requests
from collections import defaultdict
from pathlib import Path


def query(parameter: str, city: str, country: str, limit: int) -> dict:
    return {
        "query": parameter,
        "near": f"{city},{country}",
        "limit": limit,
    }
    
def get_popular_category(file_path: str = 'search_history.json') -> str:
    with open(file_path, 'r') as f:
        places = json.load(f)
    
    category_counter = defaultdict(int)
    for place in places:
        category = place.get('category')
        category_counter[category] += 1
    
    if not category_counter:
        raise ValueError("No categories found in JSON file")
    
    return max(category_counter, key=lambda k: category_counter[k])

def query_recomend(city: str, country: str, limit: int) -> dict:
    try:
        popular_category = get_popular_category()
    except (FileNotFoundError, ValueError) as e:
        # Обработка ошибок (можно задать категорию по умолчанию)
        popular_category = "shop"
    
    return {
        "category": popular_category,  # ключ должен соответствовать параметру в URL
        "near": f"{city},{country}",
        "limit": limit
    }
