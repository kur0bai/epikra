from sqlalchemy import Column, Integer, String, JSON
from app.core.database import Base


class ContentType(Base):
    __tablename__ = "content_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    fields = Column(JSON)  # [{"name": "title", "type": "string"}, ...]
