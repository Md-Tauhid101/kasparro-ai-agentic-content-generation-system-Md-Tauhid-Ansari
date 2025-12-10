from agents import (
    ParserAgent,
    QuestionAgent,
    FAQPageAgent,
    ProductPageAgent,
    ComparisonAgent
)


class Orchestrator:

    def __init__(self):
        self.parser = ParserAgent()
        self.question_agent = QuestionAgent()
        self.faq_agent = FAQPageAgent()
        self.product_agent = ProductPageAgent()
        self.comparison_agent = ComparisonAgent()

    def run_pipeline(self, raw_input: dict):
        # Step 1 — parse raw data
        product = self.parser.run(raw_input)

        # Step 2 — parallel logical branches
        questions = self.question_agent.run(product)
        faq_page = self.faq_agent.run(product, questions)

        product_page = self.product_agent.run(product)
        comparison_page = self.comparison_agent.run(product)

        # Step 3 — final output
        return {
            "faq_page": faq_page.model_dump(),
            "product_page": product_page.model_dump(),
            "comparison_page": comparison_page.model_dump()
        }
