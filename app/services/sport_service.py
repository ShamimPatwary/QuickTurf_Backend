from typing import List

from fastapi import HTTPException, status

from app.core.permissions import ensure_turf_active
from app.models.sport import Sport
from app.models.turf_admin import TurfAdmin
from app.repositories.sport_repository import SportRepository
from app.repositories.turf_repository import TurfRepository
from app.schemas.sport_schema import SportCreate, SportUpdate
from app.services.base_service import BaseService


class SportService(BaseService):
    """Turf-admin facing business logic for managing sports offered by a turf."""

    def __init__(self, db):
        super().__init__(db)
        self.sport_repo = SportRepository(db)
        self.turf_repo = TurfRepository(db)

    def create_sport(self, turf_admin: TurfAdmin, data: SportCreate) -> Sport:
        ensure_turf_active(self.db, turf_admin)
        sport = Sport(turf_id=turf_admin.turf_id, name=data.name)
        self.sport_repo.add(sport)
        self.sport_repo.commit()
        self.sport_repo.refresh(sport)
        return sport

    def list_sports(self, turf_admin: TurfAdmin) -> List[Sport]:
        return self.sport_repo.list_by_turf(turf_admin.turf_id)

    def update_sport(self, turf_admin: TurfAdmin, sport_id: int, data: SportUpdate) -> Sport:
        sport = self.sport_repo.get_by_turf(sport_id, turf_admin.turf_id)
        if not sport:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sport not found")
        for field, value in data.dict(exclude_unset=True).items():
            setattr(sport, field, value)
        self.sport_repo.commit()
        self.sport_repo.refresh(sport)
        return sport

    def delete_sport(self, turf_admin: TurfAdmin, sport_id: int) -> None:
        sport = self.sport_repo.get_by_turf(sport_id, turf_admin.turf_id)
        if not sport:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sport not found")
        self.sport_repo.delete(sport)
        self.sport_repo.commit()

