import json
from typing import TypedDict, List, Any
from langgraph.graph import StateGraph, END

from chains import (
    parser_chain,
    build_question_chain,
    build_faq_chain,
    build_product_chain,
    build_comparison_chain,
)
from models import ProductModel


# 1. THE STATE
class PipelineState(TypedDict, total=False):
    raw_input: dict
    product: dict
    questions: List[dict]
    faq_page: Any
    product_page: Any
    comparison_page: Any


# NODES
def parser_node(state: PipelineState) -> PipelineState:
    raw_json = json.dumps(state["raw_input"])

    result = parser_chain.invoke({
        "raw_json": raw_json,
        "format_instructions": "Return a ProductModel JSON."
    })

    text = result.content if hasattr(result, "content") else result

    try:
        product = ProductModel.model_validate_json(text)
        state["product"] = product.model_dump()
        return state

    except Exception:
        raw = state["raw_input"]

        fallback = ProductModel(
            product_name=raw.get("product_name", "Unknown Product"),
            concentration=raw.get("concentration"),
            concentration_pct=None,
            skin_type=raw.get("skin_type", []),
            key_ingredients=raw.get("key_ingredients", []),
            benefits=raw.get("benefits", []),
            how_to_use=raw.get("how_to_use", "Not provided."),
            side_effects=raw.get("side_effects"),
            price=raw.get("price", "Not provided"),
            meta=raw
        )

        state["product"] = fallback.model_dump()
        return state


def question_node(state: PipelineState) -> PipelineState:
    chain = build_question_chain(15)

    result = chain.invoke({
        "product_json": json.dumps(state["product"])
    })

    text = result.content if hasattr(result, "content") else result

    try:
        state["questions"] = json.loads(text)
    except Exception:
        lines = [x.strip() for x in text.split("\n") if x.strip()]
        state["questions"] = [{"question": q} for q in lines[:15]]

    return state


def faq_node(state: PipelineState) -> PipelineState:
    chain = build_faq_chain()

    result = chain.invoke({
        "product_json": json.dumps(state["product"]),
        "questions_json": json.dumps(state["questions"])
    })

    state["faq_page"] = result.dict()
    return state


def product_node(state: PipelineState) -> PipelineState:
    chain = build_product_chain()

    result = chain.invoke({
        "product_json": json.dumps(state["product"])
    })

    state["product_page"] = result.dict()
    return state


def comparison_node(state: PipelineState) -> PipelineState:
    chain = build_comparison_chain()

    product_a = state["product"]

    # Create fictional variant
    product_b = {
    "product_name": product_a["product_name"] + " Advanced Formula"
    }
    result = chain.invoke({
        "product_a_json": json.dumps(product_a),
        "product_b_json": json.dumps(product_b),
    })

    state["comparison_page"] = result.dict()
    return state


# BUILD GRAPH
graph = StateGraph(PipelineState)

graph.add_node("parse", parser_node)
graph.add_node("questions", question_node)
graph.add_node("faq", faq_node)
graph.add_node("product", product_node)
graph.add_node("comparison", comparison_node)

graph.set_entry_point("parse")

graph.add_edge("parse", "questions")
graph.add_edge("questions", "faq")
graph.add_edge("faq", "product")
graph.add_edge("product", "comparison")
graph.add_edge("comparison", END)

app = graph.compile()

# RUN PIPELINE
def run_pipeline(raw_input: dict):
    initial_state: PipelineState = {
        "raw_input": raw_input,
    }

    return app.invoke(initial_state)
