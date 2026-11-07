import os
from dotenv import load_dotenv
from sqlmodel import Session, select, func
from app.database import create_db_and_tables, engine
from app.models import User, Role
from app.security import hash_password

load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_NAME = os.getenv("ADMIN_NAME")


def seed_admin():
    create_db_and_tables()

    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        print("Error: ADMIN_EMAIL or ADMIN_PASSWORD not found in .env file!")
        return

    admin_email = ADMIN_EMAIL.strip().lower()
    admin_name = ADMIN_NAME.strip() if ADMIN_NAME else "Admin"

    with Session(engine) as session:
        existing_user = session.exec(
            select(User).where(func.lower(User.email) == admin_email)
        ).first()

        if existing_user:
            print(f"Admin with email '{admin_email}' already exists. Skipping.")
            return

        # create new admin
        admin_user = User(
            name=admin_name,
            email=admin_email,
            hashed_password=hash_password(ADMIN_PASSWORD),
            role=Role.ADMIN,
        )

        session.add(admin_user)
        session.commit()
        session.refresh(admin_user)
        print(
            f"Admin user '{admin_email}' created successfully with Role: {admin_user.role}!"
        )


if __name__ == "__main__":
    seed_admin()
