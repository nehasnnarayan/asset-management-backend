"""
Auth Router:
Handles Admin/User login, returning real JWTs with Roles and Permissions.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
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
    try:
        # 1. Ensure Roles exist
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

        # 2. Add Original Dummy Employees
        dummy_emps = [
            ("JD_001", "John", "Doe", "john@example.com"),
            ("JS_001", "Jane", "Smith", "jane@example.com"),
            ("AW_001", "Alice", "Webb", "alice@example.com"),
            ("BM_001", "Bob", "Martin", "bob@example.com"),
            ("CD_001", "Charlie", "Day", "charlie@example.com")
        ]
        emp_objects = {}
        for code, first, last, email in dummy_emps:
            emp = db.query(models.Employee).filter(models.Employee.employee_code == code).first()
            if not emp:
                emp = models.Employee(employee_code=code, first_name=first, last_name=last, email=email, designation="Staff")
                db.add(emp)
            emp_objects[code] = emp
        
        # Test accounts also need Employee profiles
        for code, first, last, email in [("SUPER_001", "System", "Superadmin", "super@example.com")]:
            emp = db.query(models.Employee).filter(models.Employee.employee_code == code).first()
            if not emp:
                emp = models.Employee(employee_code=code, first_name=first, last_name=last, email=email, designation="Admin Account")
                db.add(emp)
        db.commit()

        # 3. Add Original Dummy Assets & Assignments
        dummy_assets = [
            ("A-1029", "MacBook Pro 16", "Active", "JD_001"),
            ("A-1030", "Dell UltraSharp 27", "Active", "JS_001"),
            ("A-1031", "ErgoChair Pro", "Pending", "AW_001"),
            ("A-1032", "Lenovo ThinkPad X1", "Active", "BM_001"),
            ("A-1033", "Apple Magic Keyboard", "Returned", "CD_001")
        ]
        
        for code, name, status, emp_code in dummy_assets:
            asset = db.query(models.Asset).filter(models.Asset.asset_code == code).first()
            if not asset:
                asset = models.Asset(asset_code=code, asset_name=name, asset_category="Electronics" if "Pro" not in name else "Furniture", 
                                     asset_status="ASSIGNED" if status != "Returned" else "AVAILABLE")
                db.add(asset)
                db.flush() # Get ID
            
            # Create Assignment
            existing = db.query(models.AssetAssignment).filter(models.AssetAssignment.asset_id == asset.asset_id).first()
            if not existing:
                assignment = models.AssetAssignment(
                    asset_id=asset.asset_id,
                    employee_id=emp_objects[emp_code].employee_id,
                    assignment_date=func.now(),
                    assignment_status=status
                )
                db.add(assignment)
        
        # 4. Fill to reach high numbers (~1245 Total)
        current_assets = db.query(models.Asset).count()
        target_assets = 1245
        if current_assets < target_assets:
            batch = []
            for i in range(current_assets, target_assets):
                # Distribute statuses to match card counts: 890 Assigned, 230 Available, 125 Maintenance
                if i < 890: status = "ASSIGNED"
                elif i < 890 + 230: status = "AVAILABLE"
                else: status = "MAINTENANCE"
                
                batch.append(models.Asset(
                    asset_code=f"BULK-{i:04d}",
                    asset_name=f"Standard Issue Asset {i}",
                    asset_category="Other",
                    asset_status=status
                ))
                if len(batch) >= 100:
                    db.add_all(batch)
                    batch = []
                    db.flush()
            if batch:
                db.add_all(batch)
        
        db.commit()
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
        
    return {"message": "Setup complete. Original dummy data and bulk assets have been populated."}

@router.post("/logout")
def logout():
    """
    Logout Endpoint.
    Simulates invalidating a token on the client-side.
    """
    return {"message": "Successfully logged out"}
