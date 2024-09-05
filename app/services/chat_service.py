# services/chat_service.py
from typing import List
from app.schemas.document import Document as DocumentSchema
from app.repositories.document_repository import InterfaceDocumentRepository
from app.services import user_service
from app.services.openai_service import generate_embeddings, chat_with_gpt
from dataclasses import dataclass
from app.repositories.user_repository import InterfaceUserRepository



@dataclass
class ChatService:
    document_repo: InterfaceDocumentRepository
    user_repo: InterfaceUserRepository
    

    async def get_relevant_documents(self, user_id: int, query_embedding: List[float]) -> List[DocumentSchema]:
        return await self.document_repo.get_documents_by_similarity(user_id=user_id, embedding=query_embedding)

    async def generate_response(self, context: str, query: str) -> str:
        return await chat_with_gpt(context, query)

    async def chat_with_rag(self, query: str, user_id: int) -> dict:
        embedding = await generate_embeddings(query)
        closest_documents = await self.get_relevant_documents(user_id, embedding)
        context = " ".join([doc.content for doc in closest_documents])
           # Construct the prompt with a system message        
        system_prompt = await self.user_repo.get_prompt_by_id(user_id)
        prompt = f"{system_prompt}\n\nContext:\n{context}\n\nQuestion: {query}"
        response = await self.generate_response(prompt)
        return {"response": response}
