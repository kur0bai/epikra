from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.dependencies.permissions import is_owner_or_admin
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.core.logger import logger
from typing import List, Optional
from app.dependencies.emojis import EmojiType


"""
    Base CRUD functions to perform the users actions
"""


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
        logger.info(f"{EmojiType.SUCCESS} User created: {user.email}")
        return db_user
    except IntegrityError:
        db.rollback()
        logger.warning(
            f"{EmojiType.WARNING} Email already registered: {user.email}")
        raise ValueError("Email already registered.")
    except Exception as ex:
        db.rollback()
        logger.exception(
            f"{EmojiType.ERROR} Internal error creating the user. {ex}")
        raise ValueError("Internal error creating the User.")


def get_user_by_username(db: Session, email: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if user:
        logger.info(f"{EmojiType.SEARCH} User found: {email}")
    else:
        logger.info(f"{EmojiType.NO_RESULTS} User not found: {email}")
    return user


def get_user_by_id(db: Session, id: str) -> Optional[User]:
    user = db.query(User).filter(User.id == id).first()
    if user:
        logger.info(f"{EmojiType.SEARCH} User found: {id}")
    else:
        logger.info(f"{EmojiType.NO_RESULTS} User not found: {id}")
    return user


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> List[User]:
    try:
        query = db.query(User)
        if search:
            query = query.filter(User.full_name.ilike(f"%{search}"))

        users = query.offset(skip).limit(limit).all()
        logger.info(f"{EmojiType.SUCCESS} Users fetched: {len(users)}")
        return users
    except Exception as ex:
        db.rollback()
        logger.exception(
            f"{EmojiType.ERROR} Internal error fetching the users. {ex}")
        raise ValueError("Internal error fetching the users.")


def update_user(db: Session, user_id: str,
                user_data: UserUpdate,
                current_user: User = Depends(lambda: is_owner_or_admin(id)
                                             )):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {id} not found"
            )
        update_user = user_data.model_dump(exclude_unset=True)
        for key, value in update_user.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        logger.info(f"{EmojiType.SUCCESS} User updated: {user.email}")
        return user
    except Exception as ex:
        db.rollback()
        logger.exception(
            f"{EmojiType.ERROR} Internal error updating the user. {ex}")
        raise ValueError("Internal error updating the user.")


def delete_user(db: Session, user_id: str,
                current_user: User = Depends(lambda: is_owner_or_admin(id))
                ):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {id} not found"
            )
        db.delete(user)
        db.commit()
        logger.info(f"{EmojiType.SUCCESS} User deleted: {user.email}")
        return user
    except Exception as ex:
        db.rollback()
        logger.exception(
            f"{EmojiType.ERROR} Internal error deleting the user. {ex}")
        raise ValueError("Internal error deleting the user.")
