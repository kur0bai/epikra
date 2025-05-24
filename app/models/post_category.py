from sqlalchemy import Table, Column, Integer, ForeignKey, String
from app.core.database import Base

""" 
    We can have different categories for posts, many to many ;)
"""

post_category = Table(
    "post_category",
    Base.metadata,
    Column("post_id", String, ForeignKey("posts.id")),
    Column("category_id", String, ForeignKey("categories.id")),
)
