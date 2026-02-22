"""
Employees Router:
CRU operations for managing employees within the firm.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
import models, schemas, database

router = APIRouter(
    prefix="/api/employees",
    tags=["Employee Management"]
)

@router.post("/", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)) -> Any:
    """
    Add a new employee.
    
    - **employee_code**: Unique employee ID/Code.
    - **first_name**: Employee's First name.
    - **last_name**: Employee's Last name.
    - **email**: Unique Email address.
    - **department_id**: Foreign key mapping to Departments table.
    - **designation**: Job Role / Title.
    """
    db_emp = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if db_emp:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    new_employee = models.Employee(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.get("/", response_model=List[schemas.EmployeeResponse])
def get_all_employees(db: Session = Depends(database.get_db)) -> Any:
    """
    View all employees.
    
    Fetches the entire list of currently active employees.
    """
    employees = db.query(models.Employee).all()
    return employees

@router.get("/{id}", response_model=schemas.EmployeeResponse)
def get_employee(id: int, db: Session = Depends(database.get_db)) -> Any:
    """
    View specific employee details.
    
    - **id**: Numeric primary key of Employee.
    """
    employee = db.query(models.Employee).filter(models.Employee.employee_id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/{id}", response_model=schemas.EmployeeResponse)
def update_employee(id: int, emp_update: schemas.EmployeeUpdate, db: Session = Depends(database.get_db)) -> Any:
    """
    Update employee details.
    
    - **id**: Numeric primary key.
    - Accepts optional fields to update.
    """
    employee = db.query(models.Employee).filter(models.Employee.employee_id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    update_data = emp_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee, key, value)
        
    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_employee(id: int, db: Session = Depends(database.get_db)) -> Any:
    """
    Delete an employee.
    
    - **id**: Numeric database primary key for employee.
    """
    employee = db.query(models.Employee).filter(models.Employee.employee_id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}

# 15 Feature: View assignments of a specific employee
@router.get("/{id}/assignments", response_model=List[schemas.AssignmentResponse])
def get_employee_assignments(id: int, db: Session = Depends(database.get_db)) -> Any:
    """
    View assignments of a specific employee.
    
    - **id**: Numeric pk of Employee.
    Returns all assigned equipment properties.
    """
    assignments = db.query(models.AssetAssignment).filter(models.AssetAssignment.employee_id == id).all()
    return assignments
