from typing import List

from fastapi import HTTPException, status

from app.core.permissions import ensure_turf_active
from app.models.time_slot import TimeSlot
from app.models.turf_admin import TurfAdmin
from app.repositories.sport_repository import SportRepository
from app.repositories.time_slot_repository import TimeSlotRepository
from app.schemas.time_slot_schema import TimeSlotCreate, TimeSlotUpdate
from app.services.base_service import BaseService


class TimeSlotService(BaseService):
    """Turf-admin facing business logic for managing time slots under a sport."""

    def __init__(self, db):
        super().__init__(db)
        self.time_slot_repo = TimeSlotRepository(db)
        self.sport_repo = SportRepository(db)

    def _ensure_sport_belongs_to_turf(self, sport_id: int, turf_id: int):
        sport = self.sport_repo.get_by_turf(sport_id, turf_id)
        if not sport:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sport not found for this turf")
        return sport

    def create_time_slot(self, turf_admin: TurfAdmin, data: TimeSlotCreate) -> TimeSlot:
        ensure_turf_active(self.db, turf_admin)
        self._ensure_sport_belongs_to_turf(data.sport_id, turf_admin.turf_id)

        time_slot = TimeSlot(
            sport_id=data.sport_id,
            start_time=data.start_time,
            end_time=data.end_time,
            price=data.price,
        )
        self.time_slot_repo.add(time_slot)
        self.time_slot_repo.commit()
        self.time_slot_repo.refresh(time_slot)
        return time_slot

    def list_time_slots(self, turf_admin: TurfAdmin, sport_id: int) -> List[TimeSlot]:
        self._ensure_sport_belongs_to_turf(sport_id, turf_admin.turf_id)
        return self.time_slot_repo.list_by_sport(sport_id)

    def update_time_slot(self, turf_admin: TurfAdmin, time_slot_id: int, data: TimeSlotUpdate) -> TimeSlot:
        time_slot = self.time_slot_repo.get_by_id(time_slot_id)
        if not time_slot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Time slot not found")
        self._ensure_sport_belongs_to_turf(time_slot.sport_id, turf_admin.turf_id)

        for field, value in data.dict(exclude_unset=True).items():
            setattr(time_slot, field, value)
        self.time_slot_repo.commit()
        self.time_slot_repo.refresh(time_slot)
        return time_slot

    def delete_time_slot(self, turf_admin: TurfAdmin, time_slot_id: int) -> None:
        time_slot = self.time_slot_repo.get_by_id(time_slot_id)
        if not time_slot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Time slot not found")
        self._ensure_sport_belongs_to_turf(time_slot.sport_id, turf_admin.turf_id)

        self.time_slot_repo.delete(time_slot)
        self.time_slot_repo.commit()
