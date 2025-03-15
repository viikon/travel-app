import json
import requests
from collections import defaultdict
from pathlib import Path
from typing import Any
import sys
import os
from pydantic import BaseModel, Field, conint
from typing import Optional, List, Dict, Any

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

RESPONSES_FILE = Path(__file__).parent.parent.parent / "api_responses.json"

def save_api_response(response_data: dict):
    """Сохраняет ответ API в файл."""
    # Создать директорию, если не существует
    RESPONSES_FILE.parent.mkdir(exist_ok=True, parents=True)
    
    # Загрузить существующие данные или создать новые
    if RESPONSES_FILE.exists():
        try:
            with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {"responses": []}
    else:
        data = {"responses": []}
    
    # Добавить новый ответ
    data["responses"].append(response_data)
    
    # Сохранить обратно
    with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def process_categories():
    input_file = Path("api_responses.json")
    output_file = Path("search_history.json")

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Собираем уникальные категории
    unique_categories = {}
    for response in data.get("responses", []):
        for place in response.get("results", []):
            for category in place.get("categories", []):
                cat_id = str(category["id"])
                cat_name = category["name"]
                if cat_id not in unique_categories:
                    unique_categories[cat_id] = cat_name

    result = {
        "search_history": [
            {"id": cat_id, "category": cat_name}
            for cat_id, cat_name in unique_categories.items()
        ]
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def get_popular_category(file_path: str = 'search_history.json') -> str:
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Получаем список из 'search_history' (по умолчанию пустой список, если ключа нет)
    search_history = data.get("search_history", [])
    
    category_counter = defaultdict(int)
    for place in search_history:
        category = place.get('category')
        if category:  # Игнорируем записи без категории
            category_counter[category] += 1
    
    if not category_counter:
        raise ValueError("No categories found in JSON file")
    
    return max(category_counter, key=lambda k: category_counter[k])


def query(parameter: str, city: str, country: str, limit: int) -> dict:
    return {
        "query": parameter,
        "near": f"{city},{country}",
        "limit": limit,
    }


def query_recomend(city: str, country: str, limit: int) -> dict:
    try:
        popular_category = get_popular_category()
    except (FileNotFoundError, ValueError, KeyError) as e:
        popular_category = "shop"
    
    return {
        "category": popular_category,
        "near": f"{city},{country}",
        "limit": limit
    }
