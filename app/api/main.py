import os
from pydoc import doc
from fastapi import FastAPI, Depends, Form, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models import document
from app.models.user import User
from app.repositories.document_repository import DocumentRepository
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.chat_service import ChatService
from app.schemas.user import UserCreate, UserOut
from app.schemas.user import User as UserSchema, UserBase, UserLogin, Token
from app.schemas.document import Document as DocumentSchema, DocumentOut, DocumentCreate
from app.schemas.document import Document
from app.services.document_service import DocumentService
from app.db.session import async_session_maker as async_session, engine as async_engine
from app.db.base import Base
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.chat import ChatRequest
from docx import Document as DocxDocument
import fitz  # PyMuPDF.
import io

from dotenv import load_dotenv



openai_api_key = os.getenv('OPENAI_API_KEY', 'YourAPIKey')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as necessary
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


#AUTH API

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_repo = AuthRepository()
auth_service = AuthService(auth_repo)

@app.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_async_db)):
    user = await auth_service.authenticate_user(db, user.email, user.password)
    access_token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
    

@app.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    """
    Logout a user.

    Returns:
        dict: A dictionary containing a success message.
    """
    return {"message": "Logout successful"}


@app.post("/documents/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...), user_id: int = Form(...), name: str = Form(...), db: AsyncSession = Depends(get_async_db)):
    """
    Upload a new document along with the user_id in the form data.
    """
    try:
        content = await file.read()
        file_type = file.content_type

        if file_type == "text/plain":
            text_content = content.decode('utf-8')
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text_content = extract_text_from_docx(content)
        elif file_type == "application/pdf":
            text_content = extract_text_from_pdf(content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        document = DocumentCreate(content=text_content, user_id=user_id, name=name)
        repo = DocumentRepository(session=db)
        await repo.add_document(document)
        return {"message": "Document uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_text_from_docx(content: bytes) -> str:
    doc = DocxDocument(io.BytesIO(content))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(content: bytes) -> str:
    pdf_document = fitz.open(stream=content, filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text
    
@app.get("/documents/id/{user_id}", response_model=List[DocumentOut])
async def get_documents(user_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Fetch the documents for a specific user.

    Args:
        user_id (int): The user's ID.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        List[Document]: A list of documents for the user.
    """
    repo = DocumentRepository(session=db)
    service = DocumentService(document_repo=repo)
    return await service.get_documents_by_user_id(user_id)

@app.get("/documents/document/{document_id}", response_model=DocumentOut)
async def get_document(document_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Fetch a document by its ID.

    Args:
        document_id (int): The document's ID.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        Document: The document.
    """
    repo = DocumentRepository(session=db)
    service = DocumentService(document_repo=repo)
    return await service.get_document_by_id(document_id)
     
@app.get("/documents/all", response_model=List[DocumentOut])
async def get_all_documents(db: AsyncSession = Depends(get_async_db)):
    """
    Fetch all documents.

    Args:
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        List[Document]: A list of all documents.
    """
    repo = DocumentRepository(session=db)
    service = DocumentService(document_repo=repo)
    documents = await service.get_all_documents()
    return documents

@app.post("/chat", status_code=status.HTTP_200_OK)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_async_db)):
    """
    Chat with the assistant using retrieval-augmented generation (RAG).

    Args:
        request (ChatRequest): The request body containing the user's query and user ID.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_async_db).

    Returns:
        dict: A dictionary containing the assistant's response.

    Raises:
        HTTPException: If there is an error during the chat process.
    """
    try:
        document_repo = DocumentRepository(session=db)
        user_repo = UserRepository(session=db)
        service = ChatService(document_repo=document_repo, user_repo=user_repo)
        response = await service.chat_with_rag(request.query, request.user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#USER API

@app.get("/users", response_model=List[UserBase])
async def get_users(db: AsyncSession = Depends(get_async_db)):
    repo = UserRepository(session=db)
    service = UserService(user_repo=repo)
    return await service.get_users()

@app.post("/users/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    repo = UserRepository(session=db)
    service = UserService(user_repo=repo)
    return await service.create_user(user)

@app.get("/users/email/{email}", response_model=UserOut)
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_async_db)):
    repo = UserRepository(session=db)
    service = UserService(user_repo=repo)
    return await service.get_user_by_email(email)


    

    #TABLE CREATION    
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def startup_event():
        await create_tables()
        await asyncio.sleep(5)  # Wait for tables to be created before starting the application

app.add_event_handler("startup", startup_event)

