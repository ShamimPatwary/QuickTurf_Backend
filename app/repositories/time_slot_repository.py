from typing import List, Optional

from app.models.time_slot import TimeSlot
from app.repositories.base_repository import BaseRepository


class TimeSlotRepository(BaseRepository[TimeSlot]):
    model = TimeSlot

    def list_by_sport(self, sport_id: int) -> List[TimeSlot]:
        return self.db.query(TimeSlot).filter(TimeSlot.sport_id == sport_id).all()

    def list_active_by_sport(self, sport_id: int) -> List[TimeSlot]:
        return (
            self.db.query(TimeSlot)
            .filter(TimeSlot.sport_id == sport_id, TimeSlot.is_active == True)  # noqa: E712
            .all()
        )

    def get_locked(self, time_slot_id: int):
        from sqlalchemy import select

        stmt = select(TimeSlot).where(TimeSlot.id == time_slot_id).with_for_update()
        return self.db.execute(stmt).scalar_one_or_none()
