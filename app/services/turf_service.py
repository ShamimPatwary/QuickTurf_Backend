from typing import List

from fastapi import HTTPException, status

from app.models.turf import Turf, TurfImage, TurfStatus
from app.patterns.factories.turf_factory import TurfFactory
from app.repositories.turf_admin_repository import TurfAdminRepository
from app.repositories.turf_repository import TurfRepository
from app.schemas.turf_schema import TurfCreate, TurfUpdate
from app.services.base_service import BaseService


class TurfService(BaseService):
    """Platform-admin facing business logic for managing turfs and their images."""

    def __init__(self, db):
        super().__init__(db)
        self.turf_repo = TurfRepository(db)
        self.turf_admin_repo = TurfAdminRepository(db)

    def create_turf(self, data: TurfCreate) -> Turf:
        if self.turf_admin_repo.get_by_email(data.turf_admin_email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

        turf = TurfFactory.create_turf(data)
        self.turf_repo.add(turf)

        turf_admin = TurfFactory.create_turf_admin(turf.id, data)
        self.turf_admin_repo.add(turf_admin)

        self.turf_repo.commit()
        self.turf_repo.refresh(turf)
        return turf

    def list_turfs(self) -> List[Turf]:
        return self.turf_repo.list_all()

    def get_turf(self, turf_id: int) -> Turf:
        turf = self.turf_repo.get_by_id(turf_id)
        if not turf:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turf not found")
        return turf

    def update_turf(self, turf_id: int, data: TurfUpdate) -> Turf:
        turf = self.get_turf(turf_id)
        for field, value in data.dict(exclude_unset=True).items():
            setattr(turf, field, value)
        self.turf_repo.commit()
        self.turf_repo.refresh(turf)
        return turf