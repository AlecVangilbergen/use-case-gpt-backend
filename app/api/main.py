import os
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.repositories.document_repository import DocumentRepository
from app.services.chat_service import ChatService
from app.schemas.document import Document as DocumentSchema
from app.db.session import async_session_maker as async_session

openai_api_key = os.getenv('OPENAI_API_KEY', 'YourAPIKey')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_async_db():
    async with async_session() as session:
        yield session

def db_dependency():
    return Depends(get_async_db)

@app.get("/")
async def root():
    return {"message": "Welcome to the API, made with FastAPI!!"}

@app.post("/documents/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_async_db)):
    """
    Upload a new document.

    Args:
        file (UploadFile): The document file to be uploaded.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing a success message if the document is uploaded successfully.

    Raises:
        HTTPException: If there is an error uploading the document.
    """
    try:
        content = await file.read()
        document = DocumentSchema(content=content.decode('utf-8'))
        repo = DocumentRepository(session=db)
        await repo.add_document(document)
        return {"message": "Document uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", status_code=status.HTTP_200_OK)
async def chat(query: str, user_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Chat with the assistant using retrieval-augmented generation (RAG).

    Args:
        query (str): The user's query.
        user_id (int): The user's ID.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing the assistant's response.

    Raises:
        HTTPException: If there is an error during the chat process.
    """
    try:
        repo = DocumentRepository(session=db)
        service = ChatService(document_repo=repo)
        response = await service.chat_with_rag(query, user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
