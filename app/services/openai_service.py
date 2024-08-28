import os
import openai
from openai import AsyncOpenAI
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API key here
client = AsyncOpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

async def generate_embeddings(query: str, model: str = "text-embedding-ada-002") -> List[float]:
    response = await client.embeddings.create(input=query, model=model)
    return response['data'][0]['embedding']

async def chat_with_gpt(context: str, query: str, model: str = "gpt-4") -> str:
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": query}
        ]
    )
    return response['choices'][0]['message']['content']
