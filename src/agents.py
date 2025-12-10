from models import (
    ProductModel,
    QuestionModel,
    FAQPageModel,
    ProductPageModel,
    ComparisonPageModel,
    ProductPageSection
)
from templates import PRODUCT_TEMPLATE, FAQ_TEMPLATE, COMPARISON_TEMPLATE
from blocks import (
    build_benefits_block,
    build_usage_block,
    build_ingredient_block,
    build_safety_block,
    build_price_block,
    build_comparison_block
)
from llm import GroqClient


class ParserAgent:
    """Converts raw dict → validated ProductModel"""
    
    def run(self, raw: dict) -> ProductModel:
        # normalize concentration
        conc = raw.get("concentration")
        conc_pct = None
        if conc and "%" in conc:
            try:
                conc_pct = float(conc.replace("%", "").strip())
            except:
                pass

        # normalize price
        price = raw.get("price")
        if isinstance(price, str) and price.startswith("₹"):
            try:
                price = float(price.replace("₹", "").strip())
            except:
                pass

        return ProductModel(
            product_name=raw["product_name"],
            concentration=raw.get("concentration"),
            concentration_pct=conc_pct,
            skin_type=raw.get("skin_type", []),
            key_ingredients=raw.get("key_ingredients", []),
            benefits=raw.get("benefits", []),
            how_to_use=raw.get("how_to_use", ""),
            side_effects=raw.get("side_effects"),
            price=price,
            meta={"parsed": True}
        )


class QuestionAgent:
    """Generates 15 FAQ questions + answers."""

    def __init__(self):
        self.llm = GroqClient()

    def run(self, product: ProductModel) -> list[QuestionModel]:
        prompt = f"""
            Generate 15 FAQ questions and short, safe answers for a skincare product.

            Product: {product.product_name}
            Key Ingredients: {product.key_ingredients}
            Benefits: {product.benefits}
            Usage: {product.how_to_use}
            Side Effects: {product.side_effects}

            Constraints:
            - No medical claims.
            - Keep answers factual and short.
            - Each answer must be safe and non-clinical.
            Return JSON list of {{ "question": "...", "answer": "..." }}
            """

        qa_list = self.llm.ask_json(prompt)

        questions = []
        for item in qa_list:
            questions.append(
                QuestionModel(
                    question=item["question"],
                    answer=item["answer"],
                    category=None,
                    source="llm"
                )
            )

        return questions


class FAQPageAgent:
    """Assembles structured FAQ page."""

    def run(self, product: ProductModel, questions: list[QuestionModel]) -> FAQPageModel:
        return FAQPageModel(
            product_name=product.product_name,
            faqs=questions,
            summary=f"Top {len(questions)} customer questions about {product.product_name}"
        )


class ProductPageAgent:
    """Builds full product page using blocks."""

    def run(self, product: ProductModel) -> ProductPageModel:

        sections = [
            ProductPageSection(**build_benefits_block(product)),
            ProductPageSection(**build_usage_block(product)),
            ProductPageSection(**build_ingredient_block(product)),
            ProductPageSection(**build_safety_block(product)),
            ProductPageSection(**build_price_block(product)),
        ]

        return ProductPageModel(
            product_name=product.product_name,
            sections=sections,
            meta={"generated": True}
        )


class ComparisonAgent:
    """Creates Product B internally + compares it with Product A."""

    def run(self, productA: ProductModel) -> ComparisonPageModel:

        # Fake competitor product
        productB = ProductModel(
            product_name=f"{productA.product_name} Competitor",
            concentration=productA.concentration,
            concentration_pct=productA.concentration_pct - 2 if productA.concentration_pct else None,
            skin_type=productA.skin_type,
            key_ingredients=productA.key_ingredients,
            benefits=productA.benefits,
            how_to_use=productA.how_to_use,
            side_effects=productA.side_effects,
            price=float(productA.price) + 50
        )

        comparison_block = build_comparison_block(productA, productB)

        return ComparisonPageModel(
            product_name=productA.product_name,
            competitor_name=productB.product_name,
            comparisons=comparison_block["content"],
            summary="Objective comparison based on price and concentration."
        )
