from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth import get_current_user
from app.schemas.qr import QRCreate
from app.services.qrs import create_qr, generate_qr_image
from app.services.ia import generate_suggestion
from app.schemas.user import User

# protecting route
router = APIRouter(
    prefix="/private",
    tags=["Private"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/generate-qr", response_class=StreamingResponse)
def generate_qr(qr_in: QRCreate, db: Session = Depends(get_db),
                current_user=Depends(get_current_user)):
    create_qr(db, qr_in, current_user.id)
    return generate_qr_image(qr_in.data)


@router.post("/improve-content")
def improve_content(content: str, db: Session = Depends(get_db)):
    response = generate_suggestion(content)
    return response


@router.get("/profile", response_model=User,
            description="Get the authenticated user information",
            name="Read the user profile info")
def get_profile(current_user: User = Depends(get_current_user)):
    try:
        return current_user
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )

    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while getting the user."
        )
