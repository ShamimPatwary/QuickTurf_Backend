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

    def list_packages(self, turf_admin: TurfAdmin) -> List[Package]:
        return self.package_repo.list_by_turf(turf_admin.turf_id)

    def update_package(self, turf_admin: TurfAdmin, package_id: int, data: PackageUpdate) -> Package:
        package = self.package_repo.get_by_turf(package_id, turf_admin.turf_id)
        if not package:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")

        update_data = data.dict(exclude_unset=True, exclude={"sport_ids"})
        for field, value in update_data.items():
            setattr(package, field, value)

        if data.sport_ids is not None:
            package.sports = self.package_repo.get_sports_by_ids(data.sport_ids, turf_admin.turf_id)

        self.package_repo.commit()
        self.package_repo.refresh(package)
        return package

    def delete_package(self, turf_admin: TurfAdmin, package_id: int) -> None:
        package = self.package_repo.get_by_turf(package_id, turf_admin.turf_id)
        if not package:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
        self.package_repo.delete(package)
        self.package_repo.commit()
