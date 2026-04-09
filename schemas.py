from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import date, datetime

# --- Auth & RBAC Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str
    user: Any = None # Optional user info to help frontend

class TokenData(BaseModel):
    user_id: Optional[str] = None

class UserLogin(BaseModel):
    employee_code: str
    password: str

class UserCreate(BaseModel):
    employee_code: str
    password: str
    role_id: int

class RoleCreate(BaseModel):
    name: str
    permissions: List[str]

class RoleResponse(BaseModel):
    id: int
    name: str
    permissions: List[str]

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    employee_code: str
    roles: List[RoleResponse] = []

    class Config:
        from_attributes = True

# --- HR Admin Schemas (Legacy/Deprecated if replaced by User) ---
class AdminLogin(BaseModel):
    email: EmailStr
    password: str 

class AdminToken(BaseModel):
    access_token: str
    token_type: str

class AdminResponse(BaseModel):
    hr_admin_id: int
    admin_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

# --- Employee Schemas ---
class EmployeeBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None
    department_id: Optional[int] = None
    designation: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    employee_code: str

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    designation: Optional[str] = None

class EmployeeResponse(EmployeeBase):
    employee_id: int
    employee_code: str
    employment_status: str
    date_of_joining: Optional[date] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Asset Schemas ---
class AssetBase(BaseModel):
    asset_name: str
    asset_category: Optional[str] = None
    purchase_cost: Optional[float] = None
    asset_condition: Optional[str] = "GOOD"

class AssetCreate(AssetBase):
    asset_code: str
    purchase_date: Optional[date] = None

class AssetUpdate(BaseModel):
    asset_name: Optional[str] = None
    asset_category: Optional[str] = None
    asset_condition: Optional[str] = None

class AssetResponse(AssetBase):
    asset_id: int
    asset_code: str
    purchase_date: Optional[date] = None
    asset_status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Assignment Schemas ---
class AssignmentCreate(BaseModel):
    asset_id: int
    employee_id: int
    assigned_by_hr_id: int
    assignment_date: date
    remarks: Optional[str] = None

class AssignmentResponse(BaseModel):
    assignment_id: int
    asset_id: int
    employee_id: int
    assigned_by_hr_id: Optional[int] = None
    assignment_date: date
    return_date: Optional[date] = None
    assignment_status: str
    remarks: Optional[str] = None

    class Config:
        from_attributes = True

class ReturnAssetUpdate(BaseModel):
    return_date: date

# --- Dashboard & Reports Schemas ---
class DashboardCounts(BaseModel):
    total_assets: int
    assigned_assets: int
    available_assets: int
    maintenance_assets: int

# --- Asset History Schemas ---
class AssetHistoryResponse(BaseModel):
    maintenance_id: int
    asset_id: int
    maintenance_type: Optional[str] = None
    maintenance_description: Optional[str] = None
    maintenance_date: Optional[date] = None
    performed_by: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
