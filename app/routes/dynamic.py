from fastapi import FastAPI
from app.core.database import SessionLocal
from app.models.content_type import ContentType
from app.services.content_router import generate_router


def load_dynamic_routers(app: FastAPI):
    db = SessionLocal()
    content_types = db.query(ContentType).all()
    for ct in content_types:
        router = generate_router(ct.name, ct.fields)
        app.include_router(router, prefix=f"/{ct.name.lower()}")
