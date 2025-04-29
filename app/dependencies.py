from fastapi import Depends, HTTPException
from jose import JWTError
from sqlalchemy.orm import Session
from app.services.auth import oauth2_scheme, jwt, SECRET_KEY, ALGORITHM
from app.core.database import get_db
from app.models import UserDB

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
