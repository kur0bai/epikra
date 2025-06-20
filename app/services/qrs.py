from io import BytesIO
from fastapi.responses import StreamingResponse
import qrcode
from sqlalchemy.orm import Session
from app.models.qr import QR
from app.schemas.qr import QRCreate
from app.core.logger import logger


def create_qr(db: Session, qr: QRCreate, user_id: int):
    new_qr = QR(data=qr.data, user_id=user_id)
    try:
        db.add(new_qr)
        db.commit()
        db.refresh(new_qr)
        logger.info(f"✅ QR code created: {new_qr.id}")
        return new_qr
    except Exception:
        db.rollback()
        logger.exception("❌ Internal error creating the QR code.")
        raise ValueError("Internal error creating the QR code.")


def generate_qr_image(data: str) -> StreamingResponse:
    try:
        qr = qrcode.make(data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="image/png")
    except Exception:
        logger.exception("❌ Internal error creating the QR code.")
        raise BufferError("Internal error creating the QR code.")


def get_qrs_by_user(db: Session, user_id: int):
    return db.query(QR).filter(QR.user_id == user_id).all()
