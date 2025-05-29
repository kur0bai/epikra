from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class LoginData(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="johndoe@mail.com",
                            description="User email")
    password: str = Field(example="securePassword123$",
                          description="User password")
    full_name: str = Field(example="John Doe", description="User full name")


class UserDelete(BaseModel):
    id: str = Field(example="K3is2odwmrw2s_53",
                    description="User internal identifier")


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    # email: Optional[str] = None


class User(BaseModel):
    id: str
    full_name: str = Field(example="John Doe", description="User full name")
    email: str = Field(..., example="johndoe@mail.com",
                       description="User email")

    class Config:
        from_attributes: True
