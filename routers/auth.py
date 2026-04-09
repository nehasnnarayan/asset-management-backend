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
    Validates credentials using Employee ID and returns a real JWT.
    """
    user = db.query(models.User).filter(models.User.employee_code == login_data.employee_code).first()
    if not user or not bcrypt.checkpw(login_data.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
    access_token_expires = timedelta(minutes=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = dependencies.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    permissions = []
    role_names = []
    for role in user.roles:
        role_names.append(role.name)
        if role.permissions:
            permissions.extend(role.permissions)
    
    unique_permissions = list(set(permissions))
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "employee_code": user.employee_code,
            "roles": role_names,
            "permissions": unique_permissions
        }
    }

@router.post("/setup")
def setup_default_users(db: Session = Depends(database.get_db)):
    """
    Helper endpoint to seed the database with Superadmin, Admin, and Employee roles/users.
    """
    # Ensure Roles exist
    super_role = db.query(models.Role).filter(models.Role.name == "Superadmin").first()
    if not super_role:
        super_role = models.Role(name="Superadmin", permissions=["manage:super", "delete:asset", "view:inventory", "manage:users"])
        db.add(super_role)

    admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
    if not admin_role:
        admin_role = models.Role(name="Admin", permissions=["delete:asset", "view:inventory", "manage:users"])
        db.add(admin_role)
    
    emp_role = db.query(models.Role).filter(models.Role.name == "Employee").first()
    if not emp_role:
        emp_role = models.Role(name="Employee", permissions=["view:my_gear"])
        db.add(emp_role)
    db.commit()
    
    # Ensure Users exist and have roles
    super_user = db.query(models.User).filter(models.User.employee_code == "SUPER_001").first()
    if not super_user:
        hashed_pw = bcrypt.hashpw(b"super123", bcrypt.gensalt()).decode('utf-8')
        super_user = models.User(employee_code="SUPER_001", hashed_password=hashed_pw)
        db.add(super_user)
    super_user.roles = [super_role, admin_role, emp_role]

    admin_user = db.query(models.User).filter(models.User.employee_code == "ADMIN_001").first()
    if not admin_user:
        hashed_pw = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode('utf-8')
        admin_user = models.User(employee_code="ADMIN_001", hashed_password=hashed_pw)
        db.add(admin_user)
    admin_user.roles = [admin_role]
        
    emp_user = db.query(models.User).filter(models.User.employee_code == "EMP_001").first()
    if not emp_user:
        hashed_pw = bcrypt.hashpw(b"employee123", bcrypt.gensalt()).decode('utf-8')
        emp_user = models.User(employee_code="EMP_001", hashed_password=hashed_pw)
        db.add(emp_user)
    emp_user.roles = [emp_role]
        
    db.commit()
    return {"message": "Setup complete. Logins - Super (All Roles): SUPER_001 / super123 | Admin: ADMIN_001 / admin123 | Employee: EMP_001 / employee123."}

@router.post("/logout")
def logout():
    """
    Logout Endpoint.
    Simulates invalidating a token on the client-side.
    """
    return {"message": "Successfully logged out"}
