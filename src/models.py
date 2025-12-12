from pydantic import BaseModel
from typing import List, Optional, Union, Any


# ---------------------------------------------------------
# PRODUCT MODEL (from assignment)
# ---------------------------------------------------------
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



# ---------------------------------------------------------
# QUESTION MODEL
# ---------------------------------------------------------
class QuestionModel(BaseModel):
    question: str
    intent: Optional[str] = None



# ---------------------------------------------------------
# FAQ PAGE MODEL
# ---------------------------------------------------------
class FAQItem(BaseModel):
    question: str
    answer: str


class FAQPageModel(BaseModel):
    product_name: str
    faqs: List[FAQItem]



# ---------------------------------------------------------
# PRODUCT PAGE MODEL
# (must reflect ProductModel fields — NOT previous architecture)
# ---------------------------------------------------------
class ProductPageModel(BaseModel):
    product_name: str
    concentration: Optional[str]
    concentration_pct: Optional[float]
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: Optional[str]
    price: Union[str, float]
    summary: Optional[str] = None 
    meta: Optional[dict] = None

# COMPARISON PAGE MODEL
class ComparisonPoint(BaseModel):
    attribute: str
    product_a_value: Any
    product_b_value: Any


class ComparisonPageModel(BaseModel):
    product_a: ProductModel
    product_b: ProductModel
    comparisons: List[ComparisonPoint]
