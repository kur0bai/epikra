from pydantic import BaseModel


class QRCreate(BaseModel):
    data: str

# basic qr output


class QRCode(BaseModel):
    id: str
    data: str
    user_id: str

    class Config:
        from_attributes: True
