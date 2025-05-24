from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.session import Base

""" 
We can have different categories for posts, many to many ;)
"""
post_category = Table(
    "post_category",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("category_id", Integer, ForeignKey("categories.id")),
)
