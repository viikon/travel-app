def get_params(query: str, limit: int) -> dict:
    return {
        "query": query,
        "limit": limit,
    }


def filter_hotel_data(data: dict) -> dict:
    return {
        "status": data.get("status"),
        "results": {
            "hotels": data.get("results", {}).get("hotels", [])
        }
    }

