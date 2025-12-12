import json
from typing import Any

def save_json(data: Any, filename: str):
    if isinstance(data, (dict, list)):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(data))

def ensure_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]

def safe_get(d, key, default=None):
    return d.get(key, default) if isinstance(d, dict) else default
