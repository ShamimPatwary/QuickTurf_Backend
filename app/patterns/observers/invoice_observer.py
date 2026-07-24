from app.models.booking import Booking
from app.patterns.observers.observer_base import BookingObserver
from app.utils.pdf_generator import generate_invoice_pdf


class InvoiceObserver(BookingObserver):
    """Generates an invoice PDF whenever a booking is created."""

    def on_booking_created(self, booking: Booking) -> None:
        generate_invoice_pdf(booking)
