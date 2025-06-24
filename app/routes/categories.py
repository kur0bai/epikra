from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.services.categories import create_category, get_categories, update_category, delete_category, get_category_by_id
from app.dependencies.roles import require_role
from app.models.user import UserRole

router = APIRouter(tags=["Categories"], prefix="/categories")


@router.get("/", response_model=List[Category],
            name="Get list of categories",
            description="Get the categories list"
            )
def get_all(db: Session = Depends(get_db)):
    return get_categories(db)


@router.get("/{id}", response_model=Category, name="Get category by id")
def get_by_id(id: str, db: Session = Depends(get_db),):
    try:
        category = get_category_by_id(db, id)
        return category
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )


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


@router.patch("/{id}", response_model=Category, name="Update category information")
def update(id: str, category_data: CategoryUpdate,  db: Session = Depends(get_db),
           user=Depends(require_role(UserRole.ADMIN, UserRole.EDITOR))):
    try:
        updated_category = update_category(db, id, category_data)
        return updated_category
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )


@router.delete("/{id}", response_model=Category, name="Delete category")
def delete(id: str, db: Session = Depends(get_db),):
    try:
        deleted_category = delete_category(db, id)
        return deleted_category
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )
