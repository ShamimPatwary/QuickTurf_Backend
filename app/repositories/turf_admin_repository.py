from typing import Optional

from app.models.turf_admin import TurfAdmin
from app.repositories.base_repository import BaseRepository


class TurfAdminRepository(BaseRepository[TurfAdmin]):
    model = TurfAdmin

    def get_by_email(self, email: str) -> Optional[TurfAdmin]:
        return self.db.query(TurfAdmin).filter(TurfAdmin.email == email).first()
