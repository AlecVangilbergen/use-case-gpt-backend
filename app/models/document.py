from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.base import Base

class Document(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="documents")
    content = Column(String, nullable=False)
    vector_embedding = Column(Vector(1536))  # Assuming 1536-dimensional embeddings
