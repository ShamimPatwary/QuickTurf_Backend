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

    def list_memberships(self, turf_admin: TurfAdmin) -> List[Membership]:
        return self.membership_repo.list_by_turf(turf_admin.turf_id)

    def update_membership(self, turf_admin: TurfAdmin, membership_id: int, data: MembershipUpdate) -> Membership:
        membership = self.membership_repo.get_by_turf(membership_id, turf_admin.turf_id)
        if not membership:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership not found")

        update_data = data.dict(exclude_unset=True, exclude={"sport_ids"})
        for field, value in update_data.items():
            setattr(membership, field, value)

        if data.sport_ids is not None:
            membership.sports = self.membership_repo.get_sports_by_ids(data.sport_ids, turf_admin.turf_id)

        self.membership_repo.commit()
        self.membership_repo.refresh(membership)
        return membership

    def delete_membership(self, turf_admin: TurfAdmin, membership_id: int) -> None:
        membership = self.membership_repo.get_by_turf(membership_id, turf_admin.turf_id)
        if not membership:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership not found")
        self.membership_repo.delete(membership)
        self.membership_repo.commit()
