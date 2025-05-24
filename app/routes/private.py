from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.services.auth import get_current_user
from app.schemas.qr import QRCreate
from app.services.qrs import create_qr, generate_qr_image

# protecting route
router = APIRouter(
    prefix="/private",
    tags=["Private"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/generate", response_class=StreamingResponse)
def generate_qr(qr_in: QRCreate, db: Session = Depends(get_db),
                current_user=Depends(get_current_user)):
    create_qr(db, qr_in, current_user.id)
    return generate_qr_image(qr_in.data)


@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "name": current_user.full_name,
        "role": current_user.role
    }
