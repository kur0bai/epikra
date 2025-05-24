import datetime
from pydantic import BaseModel
from app.models.post import PostStatus
from typing import List

from app.schemas.category import Category


class PostBase(BaseModel):
    title: str
    slug: str
    content: str
    status: str = PostStatus.DRAFT


class PostCreate(PostBase):
    category_ids: List[str]


class Post(PostBase):
    id: str
    created_at: datetime
    updated_at: datetime
    categories: List[Category]

    class Config:
        orm_mode = True
