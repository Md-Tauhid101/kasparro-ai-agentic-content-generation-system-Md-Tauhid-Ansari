def build_benefits_block(product):
    benefits = list(dict.fromkeys(product.benefits))  # remove duplicates

    items = []
    for b in benefits:
        items.append({"headline": b})

    return {
        "block_type": "benefits",
        "title": "Key Benefits",
        "content": items
    }

def build_usage_block(product):
    raw = product.how_to_use

    steps = []
    for s in raw.replace("•", ".").split("."):
        if s.strip():
            steps.append(s.strip())

    return {
        "block_type": "usage",
        "title": "How to Use",
        "content": {
            "steps": steps
        }
    }

def build_ingredient_block(product):
    items = []
    for ing in product.key_ingredients:
        items.append({"name": ing})

    return {
        "block_type": "ingredients",
        "title": "Key Ingredients",
        "content": items
    }

def build_safety_block(product):
    text = product.side_effects or "No major side effects reported. Patch test recommended."

    return {
        "block_type": "safety",
        "title": "Safety Information",
        "content": {"description": text}
    }

def build_price_block(product):
    price_value = product.price

    return {
        "block_type": "price",
        "title": "Pricing",
        "content": {
            "price": price_value,
            "currency": "INR"  
        }
    }

def build_comparison_block(productA, productB):
    comparisons = []

    # price comparison
    if productA.price and productB.price:
        verdict = ()
        if productA.price < productB.price:
            verdict = "cheaper"
        elif productA.price > productB.price:
            verdict = "More expensive"
        else:
            verdict = "Same price"
            
        comparisons.append({
            "attribute": "Price",
            "product_value": productA.price,
            "competitor_value": productB.price,
            "verdict": verdict
        })

    # concentration comparison
    if productA.concentration_pct and productB.concentration_pct:
        if productA.concentration_pct > productB.concentration_pct:
            v = "Higher concentration"
        elif productA.concentration_pct < productB.concentration_pct:
            v = "Lower concentration"
        else:
            v = "Same concentration"

        comparisons.append({
            "attribute": "Vitamin C %",
            "product_value": productA.concentration_pct,
            "competitor_value": productB.concentration_pct,
            "verdict": v
        })

    return {
        "block_type": "comparison",
        "title": f"Comparison: {productA.product_name} vs {productB.product_name}",
        "content": comparisons
    }
