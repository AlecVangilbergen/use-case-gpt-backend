from openai import AsyncOpenAI
from typing import List

openai = AsyncOpenAI(api_key="jouw-api-sleutel")  # Zorg ervoor dat je jouw OpenAI API-sleutel hier invoegt

async def generate_embeddings(query: str, model: str = "text-similarity-davinci-001") -> List[float]:
    response = await openai.embeddings.create(input=query, model=model)
    return response['data']['embeddings']

async def chat_with_gpt(context: str, query: str, model: str = "davinci") -> str:
    response = await openai.chat.completions.create(prompt=f"{context}\n\n{query}", model=model)
    return response['choices'][0]['message']['content']
