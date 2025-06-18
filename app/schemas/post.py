from datetime import datetime
from pydantic import BaseModel, Field
from app.models.post import PostStatus
from typing import List

from app.schemas.category import Category


class PostBase(BaseModel):
    title: str = Field(example="The AI hype in these times",
                       description="Title or name of post")
    slug: str = Field(example="the-ai-hype",
                      description="Slug or URL for posts reference")
    content: str = Field(example="",
                         description="Post content")
    status: str = PostStatus.DRAFT


class PostCreate(PostBase):
    category_ids: List[str]


class PostUpdate(PostBase):
    category_ids: List[str]


class PostDelete(BaseModel):
    id: str = Field(example="K3is2odwmrw2s_53",
                    description="User internal identifier")


class Post(PostBase):
    id: str
    created_at: datetime
    updated_at: datetime
    categories: List[Category]

    class Config:
        from_attributes = True
