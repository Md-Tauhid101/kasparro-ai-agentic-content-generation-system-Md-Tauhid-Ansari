import argparse
import json
from orchestrator import run_pipeline
from utils import save_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input JSON file with raw product data"
    )
    args = parser.parse_args()

    # Load raw input JSON
    with open(args.input, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # Run agentic pipeline
    outputs = run_pipeline(raw)

    # Extract final structured pages
    faq = outputs.get("faq_page")
    product_page = outputs.get("product_page")
    comparison_page = outputs.get("comparison_page")

    # Save each output as JSON
    save_json(faq, "faq.json")
    save_json(product_page, "product_page.json")
    save_json(comparison_page, "comparison_page.json")

    print("\n✅ Pipeline finished.")
    print("📁 Files saved:")
    print("   - faq.json")
    print("   - product_page.json")
    print("   - comparison_page.json\n")


if __name__ == "__main__":
    main()
