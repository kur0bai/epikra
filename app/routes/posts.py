from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.roles import require_role
from app.models.user import UserRole
from app.schemas.post import PostCreate, Post, PostUpdate
from app.services.posts import create_post, get_posts, update_post, delete_post, get_post_by_id

router = APIRouter(tags=["Posts"], prefix="/posts")


@router.get("/", response_model=List[Post],
            name="Get list of posts",
            description="Get the post list"
            )
def get_all(db: Session = Depends(get_db)):
    return get_posts(db)


@router.get("/{id}", response_model=Post, name="Get post by id")
def get_by_id(id: str, db: Session = Depends(get_db),):
    try:
        post = get_post_by_id(db, id)
        return post
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )


@router.post("/", response_model=Post)
def create(post: PostCreate, db: Session = Depends(get_db),
           user=Depends(require_role(UserRole.ADMIN, UserRole.EDITOR))):
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


@router.patch("/{id}", response_model=Post, name="Update post information")
def update(id: str, post_data: PostUpdate,  db: Session = Depends(get_db),
           user=Depends(require_role(UserRole.ADMIN, UserRole.EDITOR))):
    try:
        updated_user = update_post(db, id, post_data)
        return updated_user
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )


@router.delete("/{id}", response_model=Post, name="Delete post")
def delete(id: str, db: Session = Depends(get_db),):
    try:
        deleted_post = delete_post(db, id)
        return deleted_post
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )
