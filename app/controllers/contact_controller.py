from app.controllers.base_controller import BaseController
from app.schemas.contact_schema import ContactMessageCreate, ContactMessageOut
from app.services.contact_service import ContactService


class ContactController(BaseController[ContactService]):
    service_class = ContactService

    def create_message(self, data: ContactMessageCreate) -> ContactMessageOut:
        return self.service.create_message(data)
