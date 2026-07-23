import os

from fastapi import HTTPException, status

from app.config import settings
from app.repositories.booking_repository import BookingRepository
from app.services.base_service import BaseService
from app.utils.pdf_generator import generate_invoice_pdf


class InvoiceService(BaseService):
    """Generates and retrieves PDF invoice files for bookings."""

    def __init__(self, db):
        super().__init__(db)
        self.booking_repo = BookingRepository(db)

    def get_or_generate_invoice(self, booking_id: int) -> str:
        booking = self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

        file_path = os.path.join(settings.UPLOAD_DIR, "invoices", f"invoice_{booking.id}.pdf")
        if not os.path.exists(file_path):
            file_path = generate_invoice_pdf(booking)

        return file_path
