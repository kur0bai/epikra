from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def create_user(db: Session, user: UserCreate):
    try:
        db_user = User(email=user.email,password=get_password_hash(user.password), full_name=user.full_name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Email already registered")
    except Exception as ex:
        print('Exception => ', ex)
        db.rollback()
        raise ValueError("Something went wrong during user creation")

def get_user_by_username(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()