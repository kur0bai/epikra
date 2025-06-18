from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.dialects.postgresql import BOOLEAN, FLOAT
from app.core.database import engine

type_map = {
    "string": String,
    "number": FLOAT,
    "boolean": BOOLEAN,
    "text": String,
    "date": String,
}


def create_dynamic_table(name: str, fields: list[dict]):
    metadata = MetaData()
    columns = [Column("id", Integer, primary_key=True)]

    for field in fields:
        field_type = type_map.get(field["type"], String)
        columns.append(Column(field["name"], field_type))

    table = Table(name.lower(), metadata, *columns)
    metadata.create_all(tables=[table], bind=engine)
    return table
