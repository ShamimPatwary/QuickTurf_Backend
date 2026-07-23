"""
Seed the first QuickTurf platform (super) admin.

There is no signup endpoint for platform admins by design — this script
is the supported way to create the first one directly in the database.

Usage:
    python seed_admin.py
    python seed_admin.py --name "Super Admin" --email admin@quickturf.com --password yourpassword

If --email/--password are omitted, you will be prompted interactively.
"""

import argparse
import getpass
import sys

from app.core.security import hash_password
from app.database import SessionLocal
from app.models.admin import Admin


def parse_args():
    parser = argparse.ArgumentParser(description="Seed the first QuickTurf platform admin")
    parser.add_argument("--name", default="Super Admin", help="Display name (default: 'Super Admin')")
    parser.add_argument("--email", help="Admin login email")
    parser.add_argument("--password", help="Admin login password")
    return parser.parse_args()


def main():
    args = parse_args()

    email = args.email or input("Admin email: ").strip()
    password = args.password or getpass.getpass("Admin password: ")

    if not email or not password:
        print("Email and password are required.")
        sys.exit(1)

    db = SessionLocal()
    try:
        existing = db.query(Admin).filter(Admin.email == email).first()
        if existing:
            print(f"An admin with email '{email}' already exists (id={existing.id}). Nothing to do.")
            sys.exit(1)

        admin = Admin(name=args.name, email=email, hashed_password=hash_password(password))
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"Platform admin created: id={admin.id}, email={admin.email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
