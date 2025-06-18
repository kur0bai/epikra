from fastapi import Depends, HTTPException, status
from app.services.auth import get_current_user
from app.models.user import User, UserRole


def is_owner_or_admin(resource_owner_id: str,
                      current_user: User = Depends(get_current_user)):
    if current_user.role == UserRole.ADMIN:
        return current_user

    if current_user.id == resource_owner_id:
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You don't have permission to perform this action."
    )
