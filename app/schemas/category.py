from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str
    slug: str


class CategoryCreate(CategoryBase):
    name = Field(examples="Politics", description="Name or title of category")
    slug = Field(examples="category",
                 description="Slug or URL for posts reference")


class Category(CategoryBase):
    id: str

    class Config:
        orm_mode = True
