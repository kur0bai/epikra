from sqlalchemy import Column, String, ForeignKey
from app.core.database import Base
import uuid


class QR(Base):
    __tablename__ = "qrs"
    id = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    data = Column(String)
    user_id = Column(String, ForeignKey("users.id"))
