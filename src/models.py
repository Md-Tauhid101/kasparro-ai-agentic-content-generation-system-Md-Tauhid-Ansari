from pydantic import BaseModel
from typing import List, Dict, Optional, Union


# --- PRODUCT MODEL ---
class ProductModel(BaseModel):
    product_name: str
    concentration: Optional[str] = None
    concentration_pct: Optional[float] = None
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: Optional[str] = None
    price: Union[str, float]
    meta: Optional[dict] = None


# --- FAQ MODELS ---
class QuestionModel(BaseModel):
    question: str
    answer: str


class FAQPageModel(BaseModel):
    product_name: str
    faqs: List[QuestionModel]
    summary: Optional[str] = None


# --- PRODUCT PAGE MODELS ---
class ProductPageSection(BaseModel):
    block_type: str
    title: Optional[str] = None
    content: Union[Dict, List, str]


class ProductPageModel(BaseModel):
    product_name: str
    sections: List[ProductPageSection]
    meta: Optional[Dict] = None


# --- COMPARISON MODELS ---
class ComparisonItem(BaseModel):
    attribute: str
    product_value: Union[str, float, int]
    competitor_value: Union[str, float, int]
    verdict: Optional[str] = None


class ComparisonPageModel(BaseModel):
    product_name: str
    competitor_name: str
    comparisons: List[ComparisonItem]
    summary: Optional[str] = None
