from sqlalchemy import VARCHAR, Column, Integer, String, Boolean, Text
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    is_superuser = Column(Boolean, default=False)
    documents = relationship("Document", back_populates="user")

