"""
Assets Router:
Endpoints for managing assets, updating status, history tracking, and searching.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional, Any
import models, schemas, database, dependencies

router = APIRouter(
    prefix="/api/assets",
    tags=["Asset Management"]
)

@router.post("/", response_model=schemas.AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(database.get_db)) -> Any:
    """
    Add a new asset.
    
    Inserts a newly procured corporate asset into the database.
    - **asset_code**: The unique barcode or tag number.
    - **asset_name**: Name or title of the item.
    - **asset_category**: Type of asset (e.g. Laptop, Furniture).
    - **purchase_cost**: Value upon procurement.
    """
    db_asset = db.query(models.Asset).filter(models.Asset.asset_code == asset.asset_code).first()
    if db_asset:
        raise HTTPException(status_code=400, detail="Asset code already exists")
    
    new_asset = models.Asset(**asset.model_dump())
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset

@router.get("/search", response_model=List[schemas.AssetResponse])
def search_assets(
    q: Optional[str] = Query(None, description="Search keyword for name or category"),
    employee_id: Optional[int] = Query(None, description="Filter assets assigned to this employee"),
    db: Session = Depends(database.get_db)
) -> Any:
    """
    Search assets by name/type or by assigned employee.
    
    - Provides a combined query builder leveraging explicit mappings.
    """
    query = db.query(models.Asset)
    
    if q:
        query = query.filter(or_(
            models.Asset.asset_name.ilike(f"%{q}%"),
            models.Asset.asset_category.ilike(f"%{q}%")
        ))
        
    if employee_id:
        query = query.join(models.AssetAssignment).filter(models.AssetAssignment.employee_id == employee_id)
        
    return query.all()

@router.get("/", response_model=List[schemas.AssetResponse])
def get_all_assets(db: Session = Depends(database.get_db), current_user: models.User = Depends(dependencies.RequirePrivilege('view:inventory'))) -> Any:
    """
    View all assets.
    
    Retrieves the complete list of corporate assets regardless of status.
    """
    return db.query(models.Asset).all()

@router.get("/{id}", response_model=schemas.AssetResponse)
def get_asset(id: int, db: Session = Depends(database.get_db)) -> Any:
    """
    View specific asset details.
    
    - **id**: Numeric ID (PK layout equivalent).
    """
    asset = db.query(models.Asset).filter(models.Asset.asset_id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.put("/{id}", response_model=schemas.AssetResponse)
def update_asset(id: int, asset_update: schemas.AssetUpdate, db: Session = Depends(database.get_db)) -> Any:
    """
    Update basic asset information.
    
    To change statuses natively, see specific endpoints.
    """
    asset = db.query(models.Asset).filter(models.Asset.asset_id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    update_data = asset_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(asset, key, value)
        
    db.commit()
    db.refresh(asset)
    return asset

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_asset(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(dependencies.RequirePrivilege('delete:asset'))) -> Any:
    """
    Delete asset entirely.
    
    - Warning: Removes the asset entry cascading if needed.
    """
    asset = db.query(models.Asset).filter(models.Asset.asset_id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    db.delete(asset)
    db.commit()
    return {"message": "Asset deleted successfully"}

@router.put("/{id}/maintenance", response_model=schemas.AssetResponse)
def mark_asset_maintenance(id: int, db: Session = Depends(database.get_db)) -> Any:
    """
    Mark asset under maintenance.
    
    Registers status alteration structurally representing physical diagnostics.
    """
    asset = db.query(models.Asset).filter(models.Asset.asset_id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    asset.asset_status = 'MAINTENANCE'
    db.commit()
    db.refresh(asset)
    return asset

@router.put("/{id}/available", response_model=schemas.AssetResponse)
def mark_asset_available(id: int, db: Session = Depends(database.get_db)) -> Any:
    """
    Mark asset available.
    
    Returns asset pool state back to normal operational stock.
    """
    asset = db.query(models.Asset).filter(models.Asset.asset_id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    asset.asset_status = 'AVAILABLE'
    db.commit()
    db.refresh(asset)
    return asset

@router.get("/{id}/status")
def get_asset_status(id: int, db: Session = Depends(database.get_db)) -> Any:
    """
    View a specific asset's status strictly.
    """
    asset = db.query(models.Asset).filter(models.Asset.asset_id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"status": asset.asset_status}

@router.get("/{id}/history", response_model=List[schemas.AssetHistoryResponse])
def get_asset_history(id: int, db: Session = Depends(database.get_db)) -> Any:
    """
    View history of an asset natively logged via maintenance tracking.
    """
    history = db.query(models.AssetMaintenanceLog).filter(models.AssetMaintenanceLog.asset_id == id).all()
    return history
