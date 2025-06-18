from pydantic import create_model
from typing import Dict, Any


def build_model(name: str, fields: list[Dict[str, Any]]):
    type_map = {
        "string": (str, ...),
        "text": (str, ...),
        "number": (float, ...),
        "boolean": (bool, ...),
        "date": (str, ...)
    }
    model_fields = {
        field["name"]: type_map[field["type"]] for field in fields
    }
    return create_model(name, **model_fields)
