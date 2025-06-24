from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(example="Politics",
                      description="Name or title of category")
    slug: str = Field(example="politics",
                      description="Slug or URL for categories reference")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase):
    id: str

    class Config:
        from_attributes: True
