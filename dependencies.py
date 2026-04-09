from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
import os
from typing import Optional

import database
import models

SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key-for-asset-track-pro")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 day

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = str(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

class RequirePrivilege:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, current_user: models.User = Depends(get_current_user)):
        # Aggregate permissions from all roles
        all_permissions = []
        for role in current_user.roles:
            if role.permissions:
                all_permissions.extend(role.permissions)
        
        if self.required_permission not in all_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required privilege: {self.required_permission}"
            )
        
        return current_user

class RequireRole:
    def __init__(self, required_role: str):
        self.required_role = required_role

    def __call__(self, current_user: models.User = Depends(get_current_user)):
        user_roles = [r.name for r in current_user.roles]
        
        if self.required_role not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Unauthorized. Required role: {self.required_role}"
            )
        
        return current_user
