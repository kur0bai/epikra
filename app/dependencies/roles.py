

from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.services.auth import get_current_user


"""
    Role decorator to handle actions by each one
"""


def require_role(*roles: str):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return user
    return wrapper
