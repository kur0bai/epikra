
from typing import Optional
from sqlalchemy.orm import Session
from app.dependencies.slug import generate_slug
from app.schemas.post import PostCreate
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


def get_post_by_slug(db: Session, slug: str) -> Optional[Post]:
    post = db.query(Post).filter(Post.slug == slug).first()
    if post:
        logger.info(f"🔍 Post found: {post}")
    else:
        logger.info(f"🛑 Post not found: {post}")
    return post
