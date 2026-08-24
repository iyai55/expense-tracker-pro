from pydantic import BaseModel
from openai import OpenAI
from config import Config


class ExpenseExtraction(BaseModel):
    amount: float
    merchant: str | None
    category: str
    description: str


client = OpenAI(api_key=Config.OPENAI_API_KEY)


def parse_expense(text):
    response = client.responses.parse(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": "Extract expense information from the user's text."},
            {
                "role": "user",
                "content": text,
            },
        ],
        text_format=ExpenseExtraction
    )
    return response.output_parsed
