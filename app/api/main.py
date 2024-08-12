from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db, engine
from app.db.base import Base
from app.services.chat_service import ChatService
from app.repositories.document_repository import DocumentRepository
from app.services.openai_service import generate_embeddings

app = FastAPI()

@app.post("/")
async def chat_with_rag(
    query: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Chat with the RAG system.

    Args:
        query (str): The user's query.
        db (AsyncSession): The database session.

    Returns:
        dict: The response from the RAG system.
    """
    # Mock user data
    mock_user_id = 1  # Placeholder user ID for testing

    # Generate embeddings for the query
    embedding = await generate_embeddings(query)

    # Create a repository instance
    repo = DocumentRepository(session=db)

    # Create a chat service instance
    service = ChatService(document_repo=repo)

    # Get the response from the RAG system
    response = await service.chat_with_rag(query=query, user_id=mock_user_id)

    return response

@app.on_event("startup")
async def on_startup():
    # Create database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Ensure that the database session is closed after each request
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = await call_next(request)
    if request.state.db is not None:
        await request.state.db.close()
    return response
