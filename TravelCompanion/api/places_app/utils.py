import json
import os
import sys
from collections import defaultdict
from pathlib import Path


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

RESPONSES_FILE = Path(__file__).parent.parent.parent / "api_responses.json"


def save_api_response(response_data: dict) -> None:
    """Сохраняет ответ API в файл."""
    RESPONSES_FILE.parent.mkdir(exist_ok=True, parents=True)
    
    if RESPONSES_FILE.exists():
        try:
            with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {"responses": []}
    else:
        data = {"responses": []}
    

    data["responses"].append(response_data)
    
    
    with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def process_categories() -> None:
    input_file: Path = Path("api_responses.json")
    output_file: Path = Path("search_history.json")

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
    
    search_history = data.get("search_history", [])
    
    category_counter = defaultdict(int)
    for place in search_history:
        category = place.get('category')
        if category:
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
    
def handle_saving_response(response_data: dict) -> None:
    """Обрабатывает сохранение ответа API с обработкой исключений."""
    try:
        save_api_response(response_data)  # Теперь передаём словарь
    except Exception as e:
        print(f"Ошибка при сохранении ответа: {str(e)}")
        
