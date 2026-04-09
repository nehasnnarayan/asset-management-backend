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

@dashboard_router.get("/summary")
def get_dashboard_summary(db: Session = Depends(database.get_db)) -> Any:
    """
    Get aggregated dashboard statistics.
    """
    total = db.query(models.Asset).count()
    assigned = db.query(models.Asset).filter(models.Asset.asset_status == 'ASSIGNED').count()
    available = db.query(models.Asset).filter(models.Asset.asset_status == 'AVAILABLE').count()
    maintenance = db.query(models.Asset).filter(models.Asset.asset_status == 'MAINTENANCE').count()
    
    return {
        "total_assets": total,
        "assigned_assets": assigned,
        "available_assets": available,
        "maintenance_assets": maintenance
    }

@dashboard_router.get("/recent-activities")
def get_recent_activities(db: Session = Depends(database.get_db)) -> Any:
    """
    Get the last 5 asset assignments with joined details.
    """
    activities = db.query(models.AssetAssignment).order_by(models.AssetAssignment.created_at.desc()).limit(5).all()
    
    return [
        {
            "id": a.asset.asset_code,
            "asset": a.asset.asset_name,
            "employee": f"{a.employee.first_name} {a.employee.last_name}" if a.employee.last_name else a.employee.first_name,
            "status": a.assignment_status,
            "date": a.assignment_date.isoformat()
        }
        for a in activities
    ]

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
