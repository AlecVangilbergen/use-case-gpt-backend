# repositories/document_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Protocol
from app.models.document import Document
from app.schemas.document import Document as DocumentSchema
from dataclasses import dataclass

class InterfaceDocumentRepository(Protocol):
    async def get_documents_by_similarity(self, user_id: int, embedding: List[float], limit: int = 3) -> List[DocumentSchema]:
        ...

@dataclass
class DocumentRepository(InterfaceDocumentRepository):
    session: AsyncSession

    async def get_documents_by_similarity(self, user_id: int, embedding: List[float], limit: int = 3) -> List[Document]:
        result = await self.session.execute(
            select(Document)
            .where(Document.user_id == user_id)
            .order_by(Document.vector_embedding.cosine_distance(embedding).desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def add_document(self, document: DocumentSchema) -> None:
        new_document = Document(**document.dict())
        self.session.add(new_document)
        await self.session.commit()
        await self.session.refresh(new_document)
        return new_document
