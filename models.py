from sqlalchemy import Column, Integer, String, Date, Numeric, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class Department(Base):
    __tablename__ = "departments"
    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(100), nullable=False)
    department_code = Column(String(20), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Employee(Base):
    __tablename__ = "employees"
    employee_id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    email = Column(String(150), unique=True, nullable=False)
    phone_number = Column(String(20))
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    designation = Column(String(100))
    employment_status = Column(String(50), default="ACTIVE")
    date_of_joining = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.now())

class HRAdmin(Base):
    """
    Maps to the 'hr_admins' table representing admin users.
    """
    __tablename__ = "hr_admins"
    hr_admin_id = Column(Integer, primary_key=True, index=True)
    admin_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone_number = Column(String(20))
    role = Column(String(50), default="HR_ADMIN")
    created_at = Column(TIMESTAMP, server_default=func.now())
    # Note: No password column exists in the original SQL dump.
    # We will simulate a login by email, or add a stub password check if required.

class Asset(Base):
    __tablename__ = "assets"
    asset_id = Column(Integer, primary_key=True, index=True)
    asset_code = Column(String(100), unique=True, nullable=False)
    asset_name = Column(String(150), nullable=False)
    asset_category = Column(String(100)) # e.g. 'type' from design sheet
    purchase_date = Column(Date)
    purchase_cost = Column(Numeric(12, 2))
    asset_status = Column(String(50), default="AVAILABLE") # Statuses: 'AVAILABLE', 'ASSIGNED', 'MAINTENANCE'
    asset_condition = Column(String(50), default="GOOD") # e.g. serial_no/model mapped here conceptually or we use category
    created_at = Column(TIMESTAMP, server_default=func.now())

class AssetAssignment(Base):
    __tablename__ = "asset_assignments"
    assignment_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    assigned_by_hr_id = Column(Integer, ForeignKey("hr_admins.hr_admin_id"))
    assignment_date = Column(Date, nullable=False)
    return_date = Column(Date)
    assignment_status = Column(String(50), default="ASSIGNED")
    remarks = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

class AssetMaintenanceLog(Base):
    """
    Functions structurally as the asset history per the DB dump.
    """
    __tablename__ = "asset_maintenance_logs"
    maintenance_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)
    maintenance_type = Column(String(100)) # E.g., 'ASSIGNED', 'RETURNED', 'MAINTENANCE'
    maintenance_description = Column(Text)
    maintenance_cost = Column(Numeric(12, 2))
    maintenance_date = Column(Date)
    performed_by = Column(String(150))
    created_at = Column(TIMESTAMP, server_default=func.now())

# Missing generic `asset_history` in DB dump. Using `asset_maintenance_logs` to record assignment triggers.
