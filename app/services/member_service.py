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
