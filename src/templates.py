from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from models import (
    FAQPageModel,
    ProductPageModel,
    ComparisonPageModel,
    QuestionModel,
)


# Output Parsers (Pydantic)
faq_parser = PydanticOutputParser(pydantic_object=FAQPageModel)
product_parser = PydanticOutputParser(pydantic_object=ProductPageModel)
comparison_parser = PydanticOutputParser(pydantic_object=ComparisonPageModel)
question_parser = PydanticOutputParser(pydantic_object=QuestionModel)

# FAQ TEMPLATE
FAQ_TEMPLATE = ChatPromptTemplate.from_template(
    """
    You are an expert FAQ generator.

    Given the product info:
    {product_json}

    And the list of user questions:
    {questions_json}

    Generate a structured FAQ page that matches EXACTLY the schema described in the following instructions.

    ONLY return JSON. Do NOT explain.

    FORMAT INSTRUCTIONS:
    {format_instructions}
    """
)


# PRODUCT PAGE TEMPLATE
PRODUCT_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Generate a structured Product Page using ONLY the fields from this product:

    Product JSON:
    {product_json}

    Fields available:
    - product_name
    - concentration
    - concentration_pct
    - skin_type
    - key_ingredients
    - benefits
    - how_to_use
    - side_effects
    - price
    - meta

    You MUST follow these format instructions:
    {format_instructions}

    Return ONLY JSON matching ProductPageModel.
    """
)



# COMPARISON TEMPLATE
COMPARISON_TEMPLATE = ChatPromptTemplate.from_template(
    """
    You will compare two skincare serums:

    PRODUCT A (given):
    {product_a_json}

    PRODUCT B (fictional):
    You MUST CREATE a fictional serum similar to Product A but with DIFFERENT:
    - key_ingredients
    - benefits
    - concentration or concentration_pct
    - side_effects (optional)
    - price

    Rules:
    - Product B CANNOT copy Product A's values.
    - Product B must be realistic and structured as a ProductModel.

    Return JSON matching ComparisonPageModel:

    - product_a: ProductModel
    - product_b: ProductModel
    - comparisons: list of comparison items
    - summary: optional

    Follow these format instructions:
    {format_instructions}

    Return ONLY JSON.
    """
)

# QUESTION GENERATION TEMPLATE
QUESTION_TEMPLATE = PromptTemplate(
    input_variables=["product_json", "format_instructions"],
    template="""
Generate 15 real user questions someone might ask about this skincare product.

Use ONLY the product fields below:

{product_json}

Requirements:
- Questions must be diverse (usage, benefits, safety, results, skin type suitability, ingredients).
- Keep them SHORT and NATURAL.
- Avoid repeating product facts verbatim.
- Avoid generic questions like "What is Vitamin C?"

Return ONLY a JSON LIST following these format instructions:
{format_instructions}
"""
)
