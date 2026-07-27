from typing import List

from fastapi import HTTPException, status

from app.core.permissions import ensure_turf_active
from app.models.membership import Membership
from app.models.turf_admin import TurfAdmin
from app.repositories.membership_repository import MembershipRepository
from app.schemas.membership_schema import MembershipCreate, MembershipUpdate
from app.services.base_service import BaseService

class MembershipService(BaseService):
    """Turf-admin facing business logic for managing memberships."""


    def __init__(self, db):
        super().__init__(db)
        self.membership_repo = MembershipRepository(db)

    def create_membership(self, turf_admin: TurfAdmin, data: MembershipCreate) -> Membership:
        ensure_turf_active(self.db, turf_admin)

        payload = data.dict(exclude={"sport_ids"})
        membership = Membership(turf_id=turf_admin.turf_id, **payload)

        if data.sport_ids:
            membership.sports = self.membership_repo.get_sports_by_ids(data.sport_ids, turf_admin.turf_id)

        self.membership_repo.add(membership)
        self.membership_repo.commit()
        self.membership_repo.refresh(membership)
        return membership