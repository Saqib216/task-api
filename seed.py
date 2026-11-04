import os
from app.security import hash_password
from app.models import User, Role
from sqlmodel import Session, select
from app.database import create_db_and_tables, engine
from dotenv import load_dotenv

load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_NAME = os.getenv("ADMIN_NAME")


def seed_admin():
    create_db_and_tables()

    if not ADMIN_EMAIL or not ADMIN_PASSWORD: 
        print("Error: ADMIN_EMAIL or ADMIN_PASSWORD not found in .env file!")
        return

    with Session(engine) as session:
        existing_user = session.exec(
            select(User).where(User.email == ADMIN_EMAIL)
        ).first()

        if existing_user:
            print(f"Admin with email '{ADMIN_EMAIL}' already exists. Skipping.")
            return 
            
        # create new admin
        admin_user = User(
            name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            hashed_password=hash_password(ADMIN_PASSWORD),
            role=Role.ADMIN,
        )

        session.add(admin_user)
        session.commit()
        session.refresh(admin_user)
        print(
            f"Admin user '{ADMIN_EMAIL}' created successfully with Role: {admin_user.role}!"
        )


if __name__ == "__main__":
    seed_admin()
