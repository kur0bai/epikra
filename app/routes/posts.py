from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.post import PostCreate, Post
from app.services.posts import create_post

router = APIRouter(tags=["Posts"])


@router.post("/posts", response_model=Post)
def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        new_post = create_post(db, post)
        return new_post

    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )

    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the post."
        )
