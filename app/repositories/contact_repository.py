from typing import List

from app.models.contact import ContactMessage
from app.repositories.base_repository import BaseRepository


class ContactRepository(BaseRepository[ContactMessage]):
    model = ContactMessage

    def list_all_ordered(self) -> List[ContactMessage]:
        return self.db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
