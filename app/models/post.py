from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from enum import Enum

from app.models.post_category import post_category

"""
    Post model with categories to handle the relationship with categories.
    Added status field to improve and allow control the posting 
"""


class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Post(Base):
    __tablename__ = "posts"
    id = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    title = Column(String(250), index=True)
    slug = Column(String(200), index=True, unique=True)
    content = Column(Text)
    status = Column(String, index=True, default=PostStatus.DRAFT)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))
    categories = relationship("Category", secondary=post_category,
                              back_populates="posts")  # add relation
