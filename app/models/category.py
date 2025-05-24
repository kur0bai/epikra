import datetime
import uuid
from app.core.database import Base
from sqlalchemy import DateTime, String, Column
from sqlalchemy.orm import relationship

from app.models import post_category

"""
    Category model for the database.
    This model is used to store categories for posts.
    It has a many-to-many relationship with the Post model.
"""


class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True, max=250)
    slug = Column(String, index=True, unique=True, max=250)
    description = Column(String, index=True,
                         nullable=True, max=300)  # optional
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    posts = relationship("Post", secondary=post_category,
                         back_populates="categories")
