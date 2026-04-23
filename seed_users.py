import database
from routers.auth import setup_default_users
from sqlalchemy.orm import Session

def seed():
    db: Session = database.SessionLocal()
    try:
        print("Starting database seeding...")
        result = setup_default_users(db)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
