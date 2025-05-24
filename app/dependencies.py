import random
import unicodedata
import re

from fastapi import Depends
from app.core.database import get_db
from app.services.posts import get_post_by_slug
from sqlalchemy.orm import Session


def slugify(text: str):
    """
    Helper function to convert any text in a controlled length slug 
    for future post

    Args:
        text (str): text to apply changes and convert to slug
    Returns:
        text: new slug text :D
    """

    if not isinstance(text, str):
        return  # if not is a text
    text = unicodedata.normalize("NFKD", text).encode(
        "ascii", "ignore").decode("utf-8")  # create a normalized text
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[^\w\s-]', '', text)
    text = text.strip('-')

    max_lenght = 200
    if len(text) > max_lenght:
        # validate the max length and transform if need it
        text = text[:max_lenght]
    return text


def generate_slug(title: str):
    base_slug = slugify(title)
    unique_slug = base_slug
    counter_times = 0
    max_attempts = 50
    is_unique = False
    db: Session = Depends(get_db)
    while is_unique is not True and counter_times < max_attempts:
        post = get_post_by_slug(db, unique_slug)
    return None
