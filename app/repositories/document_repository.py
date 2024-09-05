# repositories/document_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Protocol
from app.models.document import Document
from app.schemas.document import Document as DocumentSchema, DocumentCreate, DocumentOut
from dataclasses import dataclass
from app.services.openai_service import generate_embeddings

class InterfaceDocumentRepository(Protocol):
    async def get_documents_by_similarity(self, user_id: int, embedding: List[float], limit: int = 3) -> List[DocumentOut]:
        ...

@dataclass
class DocumentRepository(InterfaceDocumentRepository):
    session: AsyncSession

    async def get_documents_by_similarity(self, user_id: int, embedding: List[float]) -> List[DocumentOut]:
    # Query the count of documents for the given user_id
        count_result = await self.session.execute(
        select(func.count(Document.id))
        .where(Document.user_id == user_id)
    )
        document_count = count_result.scalar()

    # Use the document count as the limit in the similarity query
        result = await self.session.execute(
        select(Document)
        .where(Document.user_id == user_id)
        .order_by(Document.vector_embedding.cosine_distance(embedding).desc())
        .limit(document_count)
    )
        return result.scalars().all()
    
    async def get_documents_by_user_id(self, user_id: int) -> List[DocumentOut]:
        result = await self.session.execute(
            select(Document)
            .where(Document.user_id == user_id)
        )
        return result.scalars().all()
    
    async def get_all_documents(self) -> List[Document]:
        result = await self.session.execute(select(Document))
        return result.scalars().all()
    
    async def add_document(self, document: DocumentCreate) -> Document:
        # Generate embedding for the document content
        embedding = await generate_embeddings(document.content)
        
        # Create the new document with the generated embedding
        new_document = Document(
            content=document.content,
            vector_embedding=embedding,
            user_id=document.user_id
        )
        self.session.add(new_document)
        await self.session.commit()
        await self.session.refresh(new_document)
        return new_document

