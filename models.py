from database import Base

from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime



class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_username = Column(String, nullable=False)
    message = Column(String, nullable=True)
    file_url = Column(String, nullable=True)
    file_type = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    