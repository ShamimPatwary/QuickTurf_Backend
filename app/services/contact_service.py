from typing import List

from fastapi import HTTPException, status

from app.models.contact import ContactMessage
from app.repositories.contact_repository import ContactRepository
from app.schemas.contact_schema import ContactMessageCreate
from app.services.base_service import BaseService


class ContactService(BaseService):
    """Business logic for contact messages submitted via the public Contact page."""

    def __init__(self, db):
        super().__init__(db)
        self.contact_repo = ContactRepository(db)

    def create_message(self, data: ContactMessageCreate) -> ContactMessage:
        message = ContactMessage(
            name=data.name,
            email=data.email,
            message=data.message,
        )
        self.contact_repo.add(message)
        self.contact_repo.commit()
        self.contact_repo.refresh(message)
        return message

    def list_all_messages(self) -> List[ContactMessage]:
        return self.contact_repo.list_all_ordered()

    def delete_message(self, message_id: int) -> None:
        message = self.contact_repo.get_by_id(message_id)
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        self.contact_repo.delete(message)
        self.contact_repo.commit()
