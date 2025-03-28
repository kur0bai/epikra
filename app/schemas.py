from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    full_name: str
    disabled: Optional[bool] = False

class UserInDB(User):
    password: str