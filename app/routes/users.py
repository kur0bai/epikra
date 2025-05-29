from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.roles import require_role
from app.models.user import UserRole
from app.services.auth import get_current_user
from app.schemas.user import User, UserUpdate
from app.core.database import get_db
from app.services.users import delete_user, get_users, update_user
from typing import List


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=User,
            description="Get the authenticated user information",
            name="Read the user profile info")
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


@router.get("/", response_model=List[User],
            name="Get list of users",
            description="Get the users list by page"
            )
def get_all(db: Session = Depends(get_db),
            user=Depends(require_role(UserRole.ADMIN))):
    return get_users(db)


@router.patch("/{id}", response_model=User, name="Update user information")
def update(id: str, user_data: UserUpdate,  db: Session = Depends(get_db)):
    try:
        updated_user = update_user(db, id, user_data)
        return updated_user
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )


@router.delete("/{id}", response_model=User, name="Delete user")
def delete(id: str, db: Session = Depends(get_db)):
    try:
        deleted_user = delete_user(db, id)
        return deleted_user
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )
