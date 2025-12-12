from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableSequence
from templates import (
    FAQ_TEMPLATE,
    PRODUCT_TEMPLATE,
    COMPARISON_TEMPLATE,
    QUESTION_TEMPLATE,
    faq_parser,
    product_parser,
    comparison_parser,
    question_parser,
)
from llm import get_llm

llm = get_llm()


# PARSER CHAIN
PARSER_PROMPT = PromptTemplate(
    input_variables=["raw_json", "format_instructions"],
    template="""
    You are a strict JSON parser. Convert the RAW product input into a valid ProductModel JSON.

    RAW INPUT:
    {raw_json}

    Instructions:
    {format_instructions}

    When a value is a list (e.g., key_ingredients, skin_type, benefits),
    return it AS a list, NOT as a string.
    """,
)
parser_chain = (
    PARSER_PROMPT
    | llm
)

# QUESTION CHAIN  
def build_question_chain(num_questions: int = 15):
    format_instructions = question_parser.get_format_instructions()

    prompt = QUESTION_TEMPLATE.partial(
        format_instructions=format_instructions
    )

    return prompt | llm



# FAQ CHAIN
def build_faq_chain():
    parser = faq_parser
    prompt = FAQ_TEMPLATE.partial(
        format_instructions=parser.get_format_instructions()
    )
    return prompt | llm | parser



# PRODUCT PAGE CHAIN
def build_product_chain():
    format_instructions = product_parser.get_format_instructions()
    prompt = PRODUCT_TEMPLATE.partial(format_instructions=format_instructions)
    chain = (
        prompt
        | llm
        | product_parser
    )

    return chain


# COMPARISON PAGE CHAIN
def build_comparison_chain():
    prompt = COMPARISON_TEMPLATE.partial(
    format_instructions=comparison_parser.get_format_instructions()
    )
    chain = (
        prompt
        | llm
        | comparison_parser
    )

    return chain
