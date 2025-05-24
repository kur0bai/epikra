from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String
import uuid
from app.core.database import Base


"""
    Basic user information can be modified or customize
    to improve and add the fields
"""


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))  # I prefer uuid :D
    email = Column(String, unique=True, index=True)
    full_name = Column(String, unique=True, nullable=True)
    password = Column(String)
    profile_picture = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))
