from datetime import datetime, timezone
import uuid
from app.core.database import Base
from sqlalchemy import DateTime, String, Column
from sqlalchemy.orm import relationship

from app.models.post_category import post_category

"""
    Category model for the database.
    This model is used to store categories for posts.
    It has a many-to-many relationship with the Post model.
"""


class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    name = Column(String(250), index=True)
    slug = Column(String(200), index=True, unique=True)
    description = Column(String(300), index=True,
                         nullable=True, default="")  # optional
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))
    posts = relationship("Post", secondary=post_category,
                         back_populates="categories")
