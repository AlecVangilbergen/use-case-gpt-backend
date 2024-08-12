from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship

class User(Base, SQLAlchemyBaseUserTable):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    documents = relationship("Document", back_populates="user")

