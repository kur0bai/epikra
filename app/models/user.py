from sqlalchemy import Column, String
import uuid
from app.core.database import Base
  
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4())) #I prefer uuid :D
    email = Column(String, unique=True, index=True)
    full_name = Column(String, unique=True, nullable=True)
    hashed_password = Column(String)