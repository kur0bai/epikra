from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user
from app.schemas.qr import QRCreate
from app.services.qrs import create_qr, generate_qr_image

router = APIRouter()

""" @router.get("/public/qr")
def public_qr(content: str):
    try:
        functions = Functions()
        qr = functions.generate(content)
        return Response(content=qr.getvalue(), media_type="image/png")
    except Exception as ex:
        return {"error": f'Something went wrong: {ex}'} """

@router.post("/generate", response_class=StreamingResponse)
def generate_qr(qr_in: QRCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Guarda en la base de datos
    create_qr(db, qr_in, current_user.id)
    # Genera imagen QR
    return generate_qr_image(qr_in.data)    
