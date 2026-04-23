import database
import models
from sqlalchemy.orm import Session

def sync_admins():
    db: Session = database.SessionLocal()
    try:
        # Get all users with Admin or Superadmin roles
        admins = db.query(models.User).join(models.User.roles).filter(models.Role.name.in_(['Admin', 'Superadmin'])).all()
        print(f"Found {len(admins)} admin users.")

        for user in admins:
            # Find the corresponding employee
            emp = db.query(models.Employee).filter(models.Employee.employee_code == user.employee_code).first()
            if not emp:
                print(f"No employee record for {user.employee_code}")
                continue

            # Check if already in hr_admins
            hr_admin = db.query(models.HRAdmin).filter(models.HRAdmin.hr_admin_id == emp.employee_id).first()
            if not hr_admin:
                print(f"Adding {emp.first_name} {emp.last_name} as HR Admin with ID {emp.employee_id}")
                new_hr = models.HRAdmin(
                    hr_admin_id=emp.employee_id,
                    admin_name=f"{emp.first_name} {emp.last_name or ''}".strip(),
                    email=emp.email,
                    phone_number=emp.phone_number,
                    role="HR_ADMIN"
                )
                db.add(new_hr)
        
        db.commit()
        print("Sync complete.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    sync_admins()
