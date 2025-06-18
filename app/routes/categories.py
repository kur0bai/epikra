from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.category import Category, CategoryCreate
from app.services.categories import create_category
from app.dependencies.roles import require_role
from app.models.user import UserRole

router = APIRouter(tags=["Categories"], prefix="/categories")


@router.post("/", response_model=Category)
def create_new_category(
        category: CategoryCreate,
        db: Session = Depends(get_db),
        # Role decorator to validate user
        user=Depends(require_role(UserRole.ADMIN, UserRole.EDITOR)),
):
    try:
        new_category = create_category(db, category)
        return new_category

    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )

    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the category."
        )
