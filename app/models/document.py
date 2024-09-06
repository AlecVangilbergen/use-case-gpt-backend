from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.base import Base
from app.models.user import User

class Document(Base):
    __tablename__ = "document"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="documents")
    content = Column(String, nullable=False)
    vector_embedding = Column(Vector(1536))  # Assuming 1536-dimensional embeddings
