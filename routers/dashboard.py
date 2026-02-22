"""
Dashboard & Reports Routers:
Statistics grouping endpoints corresponding to analytics sections natively.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Any
import models, schemas, database

dashboard_router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard Overview"]
)

reports_router = APIRouter(
    prefix="/api/reports",
    tags=["Reports Generation"]
)

# --- Dashboard Overviews ---

@dashboard_router.get("/total-assets")
def get_total_assets(db: Session = Depends(database.get_db)) -> Any:
    """
    Get total asset count.
    
    Queries complete DB bounds for gross item count.
    """
    count = db.query(models.Asset).count()
    return {"total_assets": count}

@dashboard_router.get("/assigned-assets")
def get_assigned_assets(db: Session = Depends(database.get_db)) -> Any:
    """
    Get assigned asset count.
    """
    count = db.query(models.Asset).filter(models.Asset.asset_status == 'ASSIGNED').count()
    return {"assigned_assets": count}

@dashboard_router.get("/available-assets")
def get_available_assets(db: Session = Depends(database.get_db)) -> Any:
    """
    Get available asset count.
    """
    count = db.query(models.Asset).filter(models.Asset.asset_status == 'AVAILABLE').count()
    return {"available_assets": count}

# --- Reports Generation ---

@reports_router.get("/assets", response_model=List[schemas.AssetResponse])
def generate_asset_report(db: Session = Depends(database.get_db)) -> Any:
    """
    Generate asset report.
    
    Fetches raw un-paginated DB bounds across assets mapping globally.
    """
    return db.query(models.Asset).all()

@reports_router.get("/assignments", response_model=List[schemas.AssignmentResponse])
def generate_assignment_report(db: Session = Depends(database.get_db)) -> Any:
    """
    Generate assignment report.
    
    Cross mapping across assignment domain boundaries.
    """
    return db.query(models.AssetAssignment).all()
