"""
Auth Router:
Handles Admin login, simulating JWT creation and basic logout endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any
import models, schemas, database

router = APIRouter(
    prefix="/api/auth",
    tags=["Admin Authentication"]
)

@router.post("/login", response_model=schemas.AdminToken)
def admin_login(login_data: schemas.AdminLogin, db: Session = Depends(database.get_db)) -> Any:
    """
    Admin Login Endpoint.
    
    Validates credentials and returns a simulated token.
    - **email**: HR Admin's registered email
    - **password**: Admin password (skipped real hash check for assignment prototype)
    
    Returns standard access_token payload.
    """
    admin = db.query(models.HRAdmin).filter(models.HRAdmin.email == login_data.email).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
        
    # Validating arbitrarily assigned dummy password "admin123" for demo purposes
    if login_data.password != "admin123":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
    return {"access_token": f"fake_token_for_{admin.hr_admin_id}", "token_type": "bearer"}

@router.post("/logout")
def admin_logout() -> Any:
    """
    Admin Logout Endpoint.
    
    Simulates invalidating a token on the client-side.
    """
    return {"message": "Successfully logged out"}
