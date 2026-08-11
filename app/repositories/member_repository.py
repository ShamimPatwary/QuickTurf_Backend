from datetime import datetime, timezone
from typing import List, Optional

from app.models.member import Member, MemberStatus
from app.models.membership import Membership, membership_sports
from app.repositories.base_repository import BaseRepository


class MemberRepository(BaseRepository[Member]):
    model = Member

    def list_by_turf(self, turf_id: int) -> List[Member]:
        return self.db.query(Member).filter(Member.turf_id == turf_id).order_by(Member.created_at.desc()).all()

    def get_by_turf(self, member_id: int, turf_id: int) -> Optional[Member]:
        return self.db.query(Member).filter(Member.id == member_id, Member.turf_id == turf_id).first()

    def find_active_by_phone(self, turf_id: int, phone: str, sport_id: int) -> Optional[Member]:
        """
        Returns the active, non-expired member record for this phone number at this turf,
        whose membership covers the given sport, if one exists. Used to auto-apply the
        membership discount when a public booking is created.
        """
        now = datetime.now(timezone.utc)
        return (
            self.db.query(Member)
            .join(Membership, Member.membership_id == Membership.id)
            .join(membership_sports, membership_sports.c.membership_id == Membership.id)
            .filter(
                Member.turf_id == turf_id,
                Member.phone == phone,
                Member.status == MemberStatus.ACTIVE,
                Member.expires_at.isnot(None),
                Member.expires_at >= now,
                membership_sports.c.sport_id == sport_id,
            )
            .first()
        )

    def count_by_status(self, turf_id: int, status: MemberStatus) -> int:
        return self.db.query(Member).filter(Member.turf_id == turf_id, Member.status == status).count()

    def sum_discount_given(self, turf_id: int) -> float:
        from app.models.booking import Booking
        from sqlalchemy import func

        result = (
            self.db.query(func.coalesce(func.sum(Booking.discount_amount), 0))
            .filter(Booking.turf_id == turf_id)
            .scalar()
        )
        return result or 0
