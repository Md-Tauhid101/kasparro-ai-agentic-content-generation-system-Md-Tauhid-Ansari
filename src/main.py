import json
import sys
from orchestrator import Orchestrator
from utils import save_json


def load_input(path: str):
    """Load product input JSON from file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input.json>")
        return

    input_file = sys.argv[1]

    # Step 1 — Load input
    raw_input = load_input(input_file)

    # Step 2 — Run pipeline
    orchestrator = Orchestrator()
    result = orchestrator.run_pipeline(raw_input)

    # Step 3 — Save output files
    save_json(result["faq_page"], "output/faq.json")
    save_json(result["product_page"], "output/product_page.json")
    save_json(result["comparison_page"], "output/comparison_page.json")

    print("Pipeline completed. Output saved to /output folder.")


if __name__ == "__main__":
    main()