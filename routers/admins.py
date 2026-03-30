"""
Admins Router:
Superadmin restricted endpoints for creating and removing Admin accounts.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
import bcrypt

import models, schemas, database, dependencies

router = APIRouter(
    prefix="/api/admins",
    tags=["Superadmin Control"]
)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_admin(user: schemas.UserCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(dependencies.RequirePrivilege('manage:super'))) -> Any:
    """
    Provision a new Admin. Strictly restricted to Superadmin.
    """
    db_user = db.query(models.User).filter(models.User.employee_code == user.employee_code).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Employee code already registered")
        
    admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
    if not admin_role:
        raise HTTPException(status_code=500, detail="Admin role not found in database")
        
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_admin = models.User(employee_code=user.employee_code, hashed_password=hashed_pw, role_id=admin_role.id)
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_admin(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(dependencies.RequirePrivilege('manage:super'))) -> Any:
    """
    Revoke Admin privileges. Strictly restricted to Superadmin.
    """
    target_admin = db.query(models.User).filter(models.User.id == id).first()
    if not target_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
        
    if target_admin.role.name == "Superadmin":
        raise HTTPException(status_code=403, detail="Cannot delete a Superadmin account")
        
    db.delete(target_admin)
    db.commit()
    return {"message": "Admin account successfully revoked"}
