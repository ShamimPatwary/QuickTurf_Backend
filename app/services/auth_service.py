from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.models.admin import Admin
from app.models.turf_admin import TurfAdmin
from app.repositories.admin_repository import AdminRepository
from app.repositories.turf_admin_repository import TurfAdminRepository
from app.services.base_service import BaseService


class AuthService(BaseService):
    """Handles authentication and password management for both admin roles."""
