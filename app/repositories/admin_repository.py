from typing import Optional

from app.models.admin import Admin
from app.repositories.base_repository import BaseRepository


class AdminRepository(BaseRepository[Admin]):
    model = Admin

    def get_by_email(self, email: str) -> Optional[Admin]:
        return self.db.query(Admin).filter(Admin.email == email).first()
