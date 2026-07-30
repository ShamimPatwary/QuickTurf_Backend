from datetime import date
from typing import List, Optional

from fastapi import HTTPException, status

from app.models.membership import Membership
from app.models.package import Package
from app.models.sport import Sport
from app.models.turf import Turf, TurfStatus
from app.repositories.booking_repository import BookingRepository
from app.repositories.membership_repository import MembershipRepository
from app.repositories.package_repository import PackageRepository
from app.repositories.sport_repository import SportRepository
from app.repositories.time_slot_repository import TimeSlotRepository
from app.repositories.turf_repository import TurfRepository
from app.schemas.time_slot_schema import AvailableTimeSlotOut
from app.services.base_service import BaseService


class PublicTurfService(BaseService):
    """Public-facing business logic for browsing turfs, sports, slot availability, packages, and memberships."""

    def __init__(self, db):
        super().__init__(db)
        self.turf_repo = TurfRepository(db)
        self.sport_repo = SportRepository(db)
        self.time_slot_repo = TimeSlotRepository(db)
        self.booking_repo = BookingRepository(db)
        self.package_repo = PackageRepository(db)
        self.membership_repo = MembershipRepository(db)

    def browse_turfs(self, sport_name: Optional[str] = None) -> List[Turf]:
        turfs = self.turf_repo.list_active()
        if sport_name:
            turfs = [t for t in turfs if any(s.name.lower() == sport_name.lower() for s in t.sports)]
        return turfs

    def get_turf_detail(self, turf_id: int) -> Turf:
        turf = self.db.query(Turf).filter(Turf.id == turf_id, Turf.status == TurfStatus.ACTIVE).first()
        if not turf:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turf not found")
        return turf

    def list_turf_sports(self, turf_id: int) -> List[Sport]:
        return self.sport_repo.list_by_turf(turf_id)

    def list_available_slots(self, turf_id: int, sport_id: int, booking_date: date) -> List[AvailableTimeSlotOut]:
        sport = self.sport_repo.get_by_turf(sport_id, turf_id)
        if not sport:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sport not found for this turf")

        time_slots = self.time_slot_repo.list_active_by_sport(sport_id)
        booked_ids = self.booking_repo.booked_slot_ids(sport_id, booking_date)

        return [
            AvailableTimeSlotOut(
                id=slot.id,
                start_time=slot.start_time,
                end_time=slot.end_time,
                price=slot.price,
                is_booked=slot.id in booked_ids,
            )
            for slot in time_slots
        ]