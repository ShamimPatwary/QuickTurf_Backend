from typing import List, Optional

from app.models.membership import Membership
from app.models.sport import Sport
from app.repositories.base_repository import BaseRepository


class MembershipRepository(BaseRepository[Membership]):
    model = Membership

    def list_by_turf(self, turf_id: int) -> List[Membership]:
        return self.db.query(Membership).filter(Membership.turf_id == turf_id).all()

    def get_by_turf(self, membership_id: int, turf_id: int) -> Optional[Membership]:
        return (
            self.db.query(Membership)
            .filter(Membership.id == membership_id, Membership.turf_id == turf_id)
            .first()
        )

   
