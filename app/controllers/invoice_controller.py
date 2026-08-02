from app.controllers.base_controller import BaseController
from app.services.invoice_service import InvoiceService


class InvoiceController(BaseController[InvoiceService]):
    service_class = InvoiceService

    def get_invoice_path(self, booking_id: int) -> str:
        return self.service.get_or_generate_invoice(booking_id)
