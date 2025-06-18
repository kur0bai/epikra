from pydantic import BaseModel


class QRCreate(BaseModel):
    url: str

# basic qr output


class QRCode(BaseModel):
    id: str
    url: str
    user_id: str

    class Config:
        from_attributes: True
