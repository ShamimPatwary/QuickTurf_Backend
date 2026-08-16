from app.controllers.base_controller import BaseController
from app.services.contact_service import ContactService


class PlatformAdminContactController(BaseController[ContactService]):
    service_class = ContactService

    def list_messages(self):
        return self.service.list_all_messages()

    def delete_message(self, message_id: int) -> dict:
        self.service.delete_message(message_id)
        return {"detail": "Message deleted"}
