"""
Employees Router:
CRU operations for managing employees within the firm.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
import models, schemas, database, dependencies
import bcrypt

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
        
    import bcrypt
    # 1. Create Employee record
    employee_data = employee.dict(exclude={"password"})
    new_employee = models.Employee(**employee_data)
    db.add(new_employee)
    db.flush() # Secure the ID before continuing

    # 2. If password provided, establish User account
    if employee.password:
        hashed = bcrypt.hashpw(employee.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = models.User(
            employee_code=employee.employee_code,
            hashed_password=hashed
        )
        # Standardize with 'Employee' role
        emp_role = db.query(models.Role).filter(models.Role.name == "Employee").first()
        if emp_role:
            new_user.roles.append(emp_role)
        db.add(new_user)
        
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
        
    update_data = emp_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee, key, value)
        
    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_employee(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(dependencies.RequirePrivilege('manage:users'))) -> Any:
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
    from sqlalchemy.orm import joinedload
    assignments = db.query(models.AssetAssignment).options(joinedload(models.AssetAssignment.asset)).filter(models.AssetAssignment.employee_id == id).all()
    return assignments

@router.post("/provision-admin", response_model=schemas.EmployeeResponse)
def provision_admin(req: schemas.ProvisionAdminRequest, db: Session = Depends(database.get_db)) -> Any:
    """
    Provision a new Admin user (Superadmin only).
    Creates an Employee record and a User account with Admin role.
    """
    # 1. Check if employee already exists
    existing_emp = db.query(models.Employee).filter(models.Employee.email == req.email).first()
    if existing_emp:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Create Employee
    new_emp = models.Employee(
        employee_code=req.employee_code,
        first_name=req.first_name,
        last_name=req.last_name,
        email=req.email,
        designation=req.designation or "Administrator"
    )
    db.add(new_emp)
    db.flush()

    # 3. Create User Account
    hashed = bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = models.User(
        employee_code=req.employee_code,
        hashed_password=hashed
    )
    
    # 4. Assign Admin Role
    admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
    if admin_role:
        new_user.roles.append(admin_role)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_emp)
    return new_emp

@router.get("/admins/list", response_model=List[schemas.EmployeeResponse])
def list_admins(db: Session = Depends(database.get_db)) -> Any:
    """
    List all employees who have the Admin role.
    """
    # Join User and Employee on employee_code, filtering by Role name
    admins = db.query(models.Employee).join(
        models.User, models.Employee.employee_code == models.User.employee_code
    ).join(
        models.User.roles
    ).filter(
        models.Role.name == "Admin"
    ).all()
    
    return admins

