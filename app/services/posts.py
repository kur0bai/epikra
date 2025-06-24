
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.emojis import EmojiType
from app.dependencies.permissions import is_owner_or_admin
from app.dependencies.slug import generate_slug
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate
from app.models.post import Post
from app.models.category import Category
from app.core.logger import logger

"""
    Post module functions
"""


def create_post(db: Session, post: PostCreate):
    db_post = Post(
        title=post.title,
        slug=generate_slug(post.title, db),
        content=post.content
    )
    try:
        categories = db.query(Category).filter(
            Category.id.in_(post.category_ids)).all()
        db_post.categories = categories

        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        logger.info(f"✅ Post created: {post.title}")
        return db_post
    except Exception as ex:
        db.rollback()
        logger.exception(f"❌ Internal error creating the post. {ex}")
        raise ValueError("Internal error creating the post.")


def update_post(db: Session, post_id: str,
                post_data: PostUpdate,
                current_user: User = Depends(lambda: is_owner_or_admin(id))):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {id} not found"
            )
        updated_post = post_data.model_dump(exclude_unset=True)
        for key, value in updated_post.items():
            setattr(post, key, value)
        db.commit()
        db.refresh(post)
        logger.info(f"{EmojiType.SUCCESS} Post updated: {post.title}")
        return post
    except Exception as ex:
        db.rollback()
        logger.exception(
            f"{EmojiType.ERROR} Internal error updating the post. {ex}")
        raise ValueError("Internal error updating the post.")


def delete_post(db: Session, post_id: str,
                current_user: User = Depends(lambda: is_owner_or_admin(id))
                ):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {id} not found"
            )
        db.delete(post)
        db.commit()
        logger.info(f"{EmojiType.SUCCESS} Post deleted: {post.title}")
        return post
    except Exception as ex:
        db.rollback()
        logger.exception(
            f"{EmojiType.ERROR} Internal error deleting the post. {ex}")
        raise ValueError("Internal error deleting the post.")


def get_post_by_slug(db: Session, slug: str) -> Optional[Post]:
    post = db.query(Post).filter(Post.slug == slug).first()
    if post:
        logger.info(f"🔍 Post found: {post}")
    else:
        logger.info(f"🛑 Post not found: {post}")
    return post


def get_post_by_id(db: Session, id: str) -> Optional[Post]:
    post = db.query(Post).filter(Post.id == id).first()
    if post:
        logger.info(f"🔍 Post found: {post}")
    else:
        logger.info(f"🛑 Post not found: {post}")
    return post


def get_posts(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> List[Post]:
    try:
        query = db.query(Post)
        if search:
            query = query.filter(Post.title.ilike(f"%{search}"))

        posts = query.offset(skip).limit(limit).all()
        logger.info(f"{EmojiType.SUCCESS} Posts fetched: {len(posts)}")
        return posts
    except Exception as ex:
        db.rollback()
        logger.exception(
            f"{EmojiType.ERROR} Internal error fetching the posts. {ex}")
        raise ValueError("Internal error fetching the posts.")
