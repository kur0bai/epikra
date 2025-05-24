from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate
from app.schemas.token import Token
from app.core.database import get_db
from app.services.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

from app.schemas.user import LoginData
from app.services.users import create_user

router = APIRouter()


@router.post("/auth/login", response_model=Token)
def login_for_access_token(form_data: LoginData = Depends(),
                           db: Session = Depends(get_db)
                           ):
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")

    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=expires_delta)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(expires_delta.total_seconds())
    }


@router.post("/auth/register", response_model=User)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user_in)
        return new_user

    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )

    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the user."
        )


@router.post("/auth/logout")
def logout():
    return {"message": "Logout successful"}
