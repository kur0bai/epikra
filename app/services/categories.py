
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.emojis import EmojiType
from app.dependencies.permissions import is_owner_or_admin
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.category import Category
from app.core.logger import logger
from sqlalchemy.exc import IntegrityError
from app.dependencies.slug import generate_slug

"""
    Category module functions
"""


def get_categories(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> List[Category]:
    try:
        query = db.query(Category)
        if search:
            query = query.filter(Category.title.ilike(f"%{search}"))

        categories = query.offset(skip).limit(limit).all()
        logger.info(
            f"{EmojiType.SUCCESS} Categories fetched: {len(categories)}")
        return categories
    except Exception as ex:
        db.rollback()
        logger.exception(
            f"{EmojiType.ERROR} Internal error fetching the categories. {ex}")
        raise ValueError("Internal error fetching the categories.")


def get_category_by_id(db: Session, id: str) -> Optional[Category]:
    category = db.query(Category).filter(Category.id == id).first()
    if category:
        logger.info(f"🔍 Category found: {category}")
    else:
        logger.info(f"🛑 Category not found: {category}")
    return category


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(
        name=category.name,
        slug=generate_slug(category.name, db)  # category.slug
    )
    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        logger.info(f"✅ Category created: {category.name}")
        return db_category
    except IntegrityError as ex:
        db.rollback()
        logger.warning(f"⚠️ Category already registered: {category.name}")
        raise ValueError("Category already registered.") from ex
    except Exception as ex:
        db.rollback()
        logger.exception(f"❌ Internal error creating the category. {ex}")
        raise ValueError("Internal error creating the category.") from ex


def update_category(db: Session,
                    category_id: str,
                    category_data: CategoryUpdate,
                    current_user: User = Depends(lambda: is_owner_or_admin(id))):
    try:
        category = db.query(Category).filter(
            Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {id} not found"
            )
        updated_category = category_data.model_dump(exclude_unset=True)
        for key, value in updated_category.items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
        logger.info(f"{EmojiType.SUCCESS} Category updated: {category.title}")
        return category
    except Exception as ex:
        db.rollback()
        logger.exception(
            f"{EmojiType.ERROR} Internal error updating the category. {ex}")
        raise ValueError("Internal error updating the category.")


def delete_category(db: Session, category_id: str,
                    current_user: User = Depends(lambda: is_owner_or_admin(id))
                    ):
    try:
        category = db.query(Category).filter(
            Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {id} not found"
            )
        db.delete(category)
        db.commit()
        logger.info(f"{EmojiType.SUCCESS} Category deleted: {category.title}")
        return category
    except Exception as ex:
        db.rollback()
        logger.exception(
            f"{EmojiType.ERROR} Internal error deleting the category. {ex}")
        raise ValueError("Internal error deleting the category.")
