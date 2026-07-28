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

    def __init__(self, db):
        super().__init__(db)
        self.package_repo = PackageRepository(db)

    def create_package(self, turf_admin: TurfAdmin, data: PackageCreate) -> Package:
        ensure_turf_active(self.db, turf_admin)

        payload = data.dict(exclude={"sport_ids"})
        package = Package(turf_id=turf_admin.turf_id, **payload)

        if data.sport_ids:
            package.sports = self.package_repo.get_sports_by_ids(data.sport_ids, turf_admin.turf_id)

        self.package_repo.add(package)
        self.package_repo.commit()
        self.package_repo.refresh(package)
        return package