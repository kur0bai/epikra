from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth import get_current_user
from app.schemas.user import User


router = APIRouter()


@router.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
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
