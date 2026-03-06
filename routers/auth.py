"""
Auth Router:
Handles Admin/User login, returning real JWTs with Roles and Permissions.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import bcrypt

import models, schemas, database, dependencies

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication and RBAC"]
)

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.UserLogin, db: Session = Depends(database.get_db)):
    """
    User Login Endpoint.
    Validates credentials and returns a real JWT.
    """
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if not user or not bcrypt.checkpw(login_data.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
    access_token_expires = timedelta(minutes=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = dependencies.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    role_name = user.role.name if user.role else None
    permissions = user.role.permissions if user.role else []
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "role": role_name,
            "permissions": permissions
        }
    }

@router.post("/setup")
def setup_default_users(db: Session = Depends(database.get_db)):
    """
    Helper endpoint to seed the database with an Admin and Employee role/user.
    """
    admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
    if not admin_role:
        admin_role = models.Role(name="Admin", permissions=["delete:asset", "view:inventory", "manage:users"])
        db.add(admin_role)
    
    emp_role = db.query(models.Role).filter(models.Role.name == "Employee").first()
    if not emp_role:
        emp_role = models.Role(name="Employee", permissions=["view:my_gear"])
        db.add(emp_role)
    db.commit()
    
    admin_user = db.query(models.User).filter(models.User.email == "admin@example.com").first()
    if not admin_user:
        hashed_pw = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode('utf-8')
        admin_user = models.User(email="admin@example.com", hashed_password=hashed_pw, role_id=admin_role.id)
        db.add(admin_user)
        
    emp_user = db.query(models.User).filter(models.User.email == "employee@example.com").first()
    if not emp_user:
        hashed_pw = bcrypt.hashpw(b"employee123", bcrypt.gensalt()).decode('utf-8')
        emp_user = models.User(email="employee@example.com", hashed_password=hashed_pw, role_id=emp_role.id)
        db.add(emp_user)
        
    db.commit()
    return {"message": "Setup complete. Logins - Admin: admin@example.com / admin123. Employee: employee@example.com / employee123."}

@router.post("/logout")
def logout():
    """
    Logout Endpoint.
    Simulates invalidating a token on the client-side.
    """
    return {"message": "Successfully logged out"}
