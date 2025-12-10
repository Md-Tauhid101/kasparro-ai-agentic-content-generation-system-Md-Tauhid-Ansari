# utils.py
import json
import os
from typing import Any


def save_json(data: Any, filename: str):
    """Save Python data to a JSON file, handling Pydantic models."""
    
    # Convert pydantic models to dict
    if hasattr(data, "model_dump"):
        data = data.model_dump()

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def ensure_list(x):
    """Ensure the input is always returned as a list."""
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]


def safe_get(d: dict, key: str, default=None):
    """Safe dictionary access without raising KeyError."""
    if not isinstance(d, dict):
        return default
    return d.get(key, default)
