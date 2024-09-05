import os
import openai
from openai import AsyncOpenAI
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI API client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_embeddings(query: str, model: str = "text-embedding-ada-002") -> List[float]:
    try:
        response = await client.embeddings.create(input=query, model=model)
        return response.data[0].embedding
    except openai.OpenAIError as e:
        # Handle errors (e.g., logging, raising HTTPException, etc.)
        print(f"Error generating embeddings: {str(e)}")
        raise

async def chat_with_gpt(context: str, query: str, model: str = "gpt-4") -> str:
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        # Handle errors (e.g., logging, raising HTTPException, etc.)
        print(f"Error during chat completion: {str(e)}")
        raise
