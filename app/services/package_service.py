from typing import List

from fastapi import HTTPException, status

from app.core.permissions import ensure_turf_active
from app.models.package import Package
from app.models.turf_admin import TurfAdmin
from app.repositories.package_repository import PackageRepository
from app.schemas.package_schema import PackageCreate, PackageUpdate
from app.services.base_service import BaseService


class PackageService(BaseService):
    """Turf-admin facing business logic for managing packages."""
