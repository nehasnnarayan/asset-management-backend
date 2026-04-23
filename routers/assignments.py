"""
Assignments Router:
Operations mapping directly to the assigning logic endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Any
import models, schemas, database

router = APIRouter(
    prefix="/api/assignments",
    tags=["Asset Assignment"]
)

@router.post("", response_model=schemas.AssignmentResponse, status_code=status.HTTP_201_CREATED)
def assign_asset(assignment: schemas.AssignmentCreate, db: Session = Depends(database.get_db)) -> Any:
    """
    Assign asset to an employee.
    
    Triggers two actions:
    1. Creates a new record in AssetAssignments.
    2. Updates the linked Asset status conditionally to 'ASSIGNED' natively via code.
    3. Adds a history trace implicitly.
    """
    asset = db.query(models.Asset).filter(models.Asset.asset_id == assignment.asset_id).first()
    if not asset or asset.asset_status != 'AVAILABLE':
        raise HTTPException(status_code=400, detail="Asset not available for assignment")
    
    new_assignment = models.AssetAssignment(**assignment.dict())
    db.add(new_assignment)
    
    # Trigger 1: Change status
    asset.asset_status = 'ASSIGNED'
    
    # Trigger 2: Abstract History Log
    history_log = models.AssetMaintenanceLog(
        asset_id=asset.asset_id,
        maintenance_type='ASSIGNED',
        maintenance_description=f"Assigned to Employed ID {assignment.employee_id}",
        maintenance_date=assignment.assignment_date,
        performed_by="System Routine"
    )
    db.add(history_log)
    
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

@router.get("", response_model=List[schemas.AssignmentResponse])
def get_all_assignments(db: Session = Depends(database.get_db)) -> Any:
    """
    View all assignments mapping directly across assignments.
    """
    assignments = db.query(models.AssetAssignment).all()
    return assignments

@router.put("/{id}/return", response_model=schemas.AssignmentResponse)
def return_asset(id: int, return_data: schemas.ReturnAssetUpdate, db: Session = Depends(database.get_db)) -> Any:
    """
    Mark asset as returned.
    
    Updates assignment completion structurally and releases the asset pool instance lock.
    """
    assignment = db.query(models.AssetAssignment).filter(models.AssetAssignment.assignment_id == id).first()
    if not assignment or assignment.assignment_status == 'RETURNED':
        raise HTTPException(status_code=400, detail="Assignment invalid or already returned")
        
    asset = db.query(models.Asset).filter(models.Asset.asset_id == assignment.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Linked asset missing structurally")
        
    assignment.return_date = return_data.return_date
    assignment.assignment_status = 'RETURNED'
    asset.asset_status = 'AVAILABLE'
    
    history_log = models.AssetMaintenanceLog(
        asset_id=asset.asset_id,
        maintenance_type='RETURNED',
        maintenance_description=f"Returned on boundary condition",
        maintenance_date=return_data.return_date,
        performed_by="System Routine"
    )
    db.add(history_log)
    
    db.commit()
    db.refresh(assignment)
    return assignment
