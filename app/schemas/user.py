from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class User(BaseModel):
    id: str
    full_name: str
    email: str

    class Config:
        orm_mode: True