from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.roles import require_role
from app.models.content_type import ContentType
from app.models.user import UserRole
from app.schemas.content_type import ContentTypeCreate, ContentTypeOut
from app.services.type_registry import create_dynamic_table

router = APIRouter(tags=["Content Types"])


@router.post("/", response_model=ContentTypeOut)
def create_content_type(
    content_type: ContentTypeCreate, db: Session = Depends(get_db),
    user=Depends(require_role(UserRole.ADMIN))
):
    # Check doesnt exists
    existing = db.query(ContentType).filter_by(name=content_type.name).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Content type already exists")

    new_type = ContentType(
        name=content_type.name,
        fields=[field.dict() for field in content_type.fields]
    )

    db.add(new_type)
    db.commit()
    db.refresh(new_type)

    # Dynamic table
    create_dynamic_table(content_type.name, content_type.fields)

    return new_type


@router.get("/", response_model=list[ContentTypeOut])
def list_content_types(db: Session = Depends(get_db),
                       user=Depends(require_role(UserRole.ADMIN))):
    return db.query(ContentType).all()
