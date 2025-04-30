from pydantic import BaseModel, EmailStr

class LoginData(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
        

class User(BaseModel):
    id: str
    full_name: str
    email: str

    class Config:
        orm_mode: True