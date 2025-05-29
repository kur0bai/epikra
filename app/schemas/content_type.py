from pydantic import BaseModel
from typing import List, Literal


class FieldSchema(BaseModel):
    name: str
    type: Literal["string", "number", "boolean", "text", "date"]


class ContentTypeCreate(BaseModel):
    name: str
    fields: List[FieldSchema]


class ContentTypeOut(ContentTypeCreate):
    id: int

    class Config:
        from_attributes = True
