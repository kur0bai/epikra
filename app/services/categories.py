
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate
from app.models.category import Category
from app.core.logger import logger
from sqlalchemy.exc import IntegrityError
from app.dependencies.slug import generate_slug

"""
    Category module functions
"""


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
