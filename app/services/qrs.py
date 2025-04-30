from io import BytesIO
from fastapi.responses import StreamingResponse
import qrcode
from sqlalchemy.orm import Session
from app.models.qr import QR
from app.schemas.qr import QRCreate
       
def create_qr(db: Session, qr: QRCreate, user_id: int):
    db_qr = QR(data=qr.data, user_id=user_id)
    db.add(db_qr)
    db.commit()
    db.refresh(db_qr)
    return db_qr

def generate_qr_image(data: str) -> StreamingResponse:
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")

     
def get_qrs_by_user(db: Session, user_id: int):
           return db.query(QR).filter(QR.user_id == user_id).all()