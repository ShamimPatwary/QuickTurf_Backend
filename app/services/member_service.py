from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import HTTPException, status

from app.models.member import Member, MemberStatus
from app.models.turf import TurfStatus
from app.models.turf_admin import TurfAdmin
from app.repositories.member_repository import MemberRepository
from app.repositories.membership_repository import MembershipRepository
from app.repositories.turf_repository import TurfRepository
from app.schemas.member_schema import MemberPurchaseCreate, MembershipCheckResult
from app.services.base_service import BaseService

class MemberService(BaseService):
    """Business logic for membership purchases, turf-admin approval, and discount lookups."""

    def __init__(self, db):
        super().__init__(db)
        self.member_repo = MemberRepository(db)
        self.membership_repo = MembershipRepository(db)
        self.turf_repo = TurfRepository(db)

    def purchase_membership(self, turf_id: int, data: MemberPurchaseCreate) -> Member:
        turf = self.turf_repo.get_by_id(turf_id)
        if not turf or turf.status != TurfStatus.ACTIVE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Turf not available")

        membership = self.membership_repo.get_by_turf(data.membership_id, turf_id)
        if not membership or not membership.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership not found")

        member = Member(
            turf_id=turf_id,
            membership_id=membership.id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            amount_paid=data.amount_paid,
            transaction_id=data.transaction_id,
            status=MemberStatus.PENDING,
        )
        self.member_repo.add(member)
        self.member_repo.commit()
        self.member_repo.refresh(member)
        return member


    def list_members(self, turf_admin: TurfAdmin) -> List[Member]:
        return self.member_repo.list_by_turf(turf_admin.turf_id)

    def get_member(self, turf_admin: TurfAdmin, member_id: int) -> Member:
        member = self.member_repo.get_by_turf(member_id, turf_admin.turf_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        return member

    def update_member_status(self, turf_admin: TurfAdmin, member_id: int, new_status: MemberStatus) -> Member:
        member = self.get_member(turf_admin, member_id)

        if new_status == MemberStatus.ACTIVE and member.status != MemberStatus.ACTIVE:
            now = datetime.now(timezone.utc)
            member.starts_at = now
            member.expires_at = now + timedelta(days=member.membership.duration_days)

        member.status = new_status
        self.member_repo.commit()
        self.member_repo.refresh(member)
        return member

    def check_membership_discount(self, turf_id: int, phone: str, sport_id: int) -> MembershipCheckResult:
        """Looks up whether this phone number has an active membership covering this sport at this turf."""
        member = self.member_repo.find_active_by_phone(turf_id, phone, sport_id)
        if not member:
            return MembershipCheckResult(is_member=False)
        return MembershipCheckResult(
            is_member=True,
            discount_percentage=member.membership.discount_percentage,
            membership_name=member.membership.name,
        )