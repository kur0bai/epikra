from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.type_registry import create_dynamic_table


def generate_router(name: str, fields: list[dict]):
    router = APIRouter()
    table = create_dynamic_table(name, fields)

    @router.post("/")
    def create_entry(data: dict, db: Session = Depends(get_db)):
        db.execute(insert(table).values(**data))
        db.commit()
        return {"ok": True}

    @router.get("/")
    def get_entries(db: Session = Depends(get_db)):
        result = db.execute(select(table)).fetchall()
        return [dict(row._mapping) for row in result]

    return router
