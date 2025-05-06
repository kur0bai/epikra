from pydantic import BaseModel, EmailStr, Field

class LoginData(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="johndoe@mail.com", description="User email")
    password: str = Field(example="securePassword123$", description="User password")
    full_name: str = Field(example="John Doe", description="User full name")
        

class User(BaseModel):
    id: str
    full_name: str = Field(example="John Doe", description="User full name")
    email: str = Field(..., example="johndoe@mail.com", description="User email")

    class Config:
        orm_mode: True