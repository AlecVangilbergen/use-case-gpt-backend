from pydoc import Doc
from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import Document as DocumentSchema, DocumentOut
from typing import List


class DocumentService():
    def __init__(self, document_repo: DocumentRepository):
        self.document_repo = document_repo

    async def get_documents_by_similarity(self, user_id: int, embedding: List[float], limit: int = 3) -> List[DocumentSchema]:
        return await self.document_repo.get_documents_by_similarity(user_id, embedding, limit)

    async def get_documents_by_user_id(self, user_id: int) -> List[DocumentOut]:
        return await self.document_repo.get_documents_by_user_id(user_id)

    async def get_all_documents(self) -> List[DocumentOut]:
        return await self.document_repo.get_all_documents()

    async def add_document(self, document: DocumentSchema) -> DocumentSchema:
        return await self.document_repo.add_document(document)