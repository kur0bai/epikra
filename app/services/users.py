from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.core.logger import logger
from typing import Optional


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        password=hashed_password,
        full_name=user.full_name
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"✅ User created: {user.email}")
        return db_user
    except IntegrityError:
        db.rollback()
        logger.warning(f"⚠️ Email already registered: {user.email}")
        raise ValueError("Email already registered.")
    except Exception as ex:
        db.rollback()
        logger.exception("❌ Internal error creating the user.")
        raise ValueError("Internal error creating the User.")


def get_user_by_username(db: Session, email: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if user:
        logger.info(f"🔍 User found: {email}")
    else:
        logger.info(f"🛑 User not found: {email}")
    return user
