from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.models.admin import Admin
from app.models.turf_admin import TurfAdmin
from app.repositories.admin_repository import AdminRepository
from app.repositories.turf_admin_repository import TurfAdminRepository
from app.services.base_service import BaseService


class AuthService(BaseService):
    """Handles authentication and password management for both admin roles."""

    def __init__(self, db):
        super().__init__(db)
        self.admin_repo = AdminRepository(db)
        self.turf_admin_repo = TurfAdminRepository(db)

    def authenticate_admin(self, email: str, password: str) -> str:
        admin: Admin = self.admin_repo.get_by_email(email)
        if not admin or not verify_password(password, admin.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return create_access_token({"sub": str(admin.id), "role": "platform_admin"})

    def authenticate_turf_admin(self, email: str, password: str) -> str:
        turf_admin: TurfAdmin = self.turf_admin_repo.get_by_email(email)
        if not turf_admin or not verify_password(password, turf_admin.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return create_access_token({"sub": str(turf_admin.id), "role": "turf_admin"})

    def change_turf_admin_password(self, turf_admin: TurfAdmin, old_password: str, new_password: str) -> None:
        if not verify_password(old_password, turf_admin.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")
        turf_admin.hashed_password = hash_password(new_password)
        self.db.commit()
