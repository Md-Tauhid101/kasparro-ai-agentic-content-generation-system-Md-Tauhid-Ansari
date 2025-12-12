from typing import Dict, List
from langchain.tools import tool

@tool
def extract_ingredients(raw: Dict) -> List[str]:
    """Extract ingredient list from raw input. Deterministic."""
    ingredients = raw.get("ingredients")
    if isinstance(ingredients, str):
        items = [i.strip() for i in ingredients.split(",") if i.strip()]
        return items
    if isinstance(ingredients, list):
        return ingredients
    return []

@tool
def extract_concentration(raw: Dict) -> str:
    return raw.get("concentration") or ""

@tool
def build_benefits_block(product: Dict) -> Dict:
    """Return structured scaffolding, not finished copy."""
    return {
        "benefits": [
            {"title": "Primary benefit", "summary": "{{primary_benefit}}"},
            {"title": "Secondary benefit", "summary": "{{secondary_benefit}}"}
        ]
    }

@tool
def build_usage_block(product: Dict) -> Dict:
    return {"usage_steps": [{"step": 1, "instruction": "{{usage_1}}"}]}

@tool
def build_ingredient_block(product: Dict) -> Dict:
    ingredients = extract_ingredients(product)
    return {"ingredients": [{"name": i} for i in ingredients]}

@tool
def build_safety_block(product: Dict) -> Dict:
    return {"warnings": [{"title": "Patch test", "advice": "Do a patch test"}]}

@tool
def validate_json_schema(payload: Dict, schema_name: str) -> Dict:
    return {"ok": True}
